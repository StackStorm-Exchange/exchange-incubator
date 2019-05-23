from ns1 import NS1
import sys

from st2common.runners.base_action import Action


class NSOneBaseAction(Action):
    """ Base NSOne class for all actions
    """

    def __init__(self, config):
        """ init method, run at class creation
        """
        super(NSOneBaseAction, self).__init__(config)
        self.logger.debug('Instantiating NSOneBaseAction()')
        self.ns1base = self._init_client()

    def _init_client(self):
        """ init_client method, run at class creation
        """
        self.logger.debug('Initializing ns1 client')
        # Check if we have an API Key in config
        try:
            api_key = self.config['api_key']
        except Exception as e:
            self.logger.error('Failed to find API Key in NS1 config')
        # Load the API Key into NS1()
        try:
            ns1 = NS1(apiKey=api_key)
        except Exception as e:
            self.logger.error(e)
            sys.exit(1)
        else:
            self.logger.debug('API Key loaded')
            return ns1
