from lib import base
from lib.exception import MissingParameterError
from lib.exception import UnsupportedActionOrResourceError


class ActionManager(base.BaseAction):

    def run(self, **kwargs):
        self.logger.debug(kwargs)
        self.logger.debug(self.config)
        try:
            requested_action = kwargs.pop('action')
        except KeyError as error:
            raise MissingParameterError(
                "'%s' required parameter is missing" % error)

        # Resolve connection config
        self.init_config(
            kwargs.pop('config_profile', None))

        # Instantiating dialer
        self.init_dialer()

        # Serve Request
        try:
            [intent, resource] = requested_action.split('_')
        except ValueError:
            raise UnsupportedActionOrResourceError(
                "Requested action: '%s' \
                    is not supported currently" % requested_action)
        intent_method_name = "intent_%s" % intent
        try:
            (is_success, response) = getattr(
                self, intent_method_name)(resource, **kwargs)
        except AttributeError:
            raise UnsupportedActionOrResourceError(
                "Requested action: '%s' \
                    is not supported currently" % (requested_action))

        return (is_success, response)
