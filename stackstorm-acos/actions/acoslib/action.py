import acos_client as acos
import re
import logging

from st2actions.runners.pythonrunner import Action


class BaseAction(Action):
    DEFAULT_AXAPI_VERSION_STR = 'v3.0'
    DEFAULT_AXAPI_VERSION = acos.AXAPI_30

    def __init__(self, config):
        super(BaseAction, self).__init__(config)

        self._set_loglevel(logging.INFO)

        self.config = config

    def login(self, str_api_version):
        try:
            return acos.Client(self.config['appliance']['target'],
                               self._get_axapi_version(str_api_version),
                               self.config['appliance']['userid'],
                               self.config['appliance']['passwd'])
        except acos.errors.ACOSUnsupportedVersion as e:
            self.logger.error(e)
        except KeyError as e:
            self.logger.error(e)

    def get_object(self, base_obj, object_path):
        obj = base_obj
        for path in object_path.split('.'):
            obj = getattr(obj, path)

        return obj

    def _set_loglevel(self, level):
        for key, logger in logging.Logger.manager.loggerDict.items():
            if isinstance(logger, logging.Logger):
                logger.setLevel(level)

    def _get_axapi_version(self, api_version):
        if re.match(r'[vV]?[a-z-_]*3\.0$', str(api_version)):
            return acos.AXAPI_30
        elif re.match(r'[vV]?[a-z-_]*2\.1$', str(api_version)):
            return acos.AXAPI_21
        else:
            self.logger.warning("This uses default API version(%s), instead of specified one(%s)" %
                                (self.DEFAULT_AXAPI_VERSION_STR, str(api_version)))

            return self.DEFAULT_AXAPI_VERSION
