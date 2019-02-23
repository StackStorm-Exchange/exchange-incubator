import sys
from lib import base
from st2common.runners.base_action import Action
from lib.exception import *


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
        [intent, resource] = requested_action.split('_')
        intent_method_name = "intent_%s" % intent
        (is_success, response) = getattr(
            self,  intent_method_name)(resource, **kwargs)

        return (is_success, response)
