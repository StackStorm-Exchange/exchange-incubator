import redis

__all__ = [
    'BaseRedisAction'
]


class Action(object):
    def __init__(self, config):
        self.config = config


class BaseRedisAction(Action):
    def __init__(self, config):
        super(BaseRedisAction, self).__init__(config=config)
        self._client = self._get_client()

    def _get_client(self):
        config = self.config

        client = redis.StrictRedis(host=config['host'], port=config['port'],
                                   db=config['database'])

        return client
