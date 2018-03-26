from lib.base import BaseRedisAction

__all__ = [
    'DelRedisAction'
]


class DelRedisAction(BaseRedisAction):
    def run(self, key):
        self._client.delete(key)
