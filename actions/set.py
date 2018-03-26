from lib.base import BaseRedisAction

__all__ = [
    'SetRedisAction'
]


class SetRedisAction(BaseRedisAction):
    def run(self, key, value, ex=None, px=None, nx=False, xx=False):
        self._client.set(key, value, ex=ex, px=px, nx=nx, xx=xx)
