import uuid

import kayako

__all__ = [
    'BaseKayakoAction'
]

class Action(object):
    def __init__(self, config):
        self.config = config


class BaseKayakoAction(Action):
    def __init__(self, config):
        super(BaseKayakoAction, self).__init__(config=config)
        self._client = self._get_client()

    def _get_client(self):
        config = self.config
        client = kayako.KayakoAPI(config['url'], config['api_key'], config['secret_key'])
        return client
