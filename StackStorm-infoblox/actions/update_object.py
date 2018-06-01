from lib.action import InfobloxBaseAction

__all__ = [
    'UpdateObjectAction',
]

class UpdateObjectAction(InfobloxBaseAction):
    def run(self, ref, **kwargs):
        _keys = list(kwargs.keys())
        for k in _keys:
            if kwargs[k] is None:
                del kwargs[k]
        result = self.connection.update_object(ref=ref, kwargs)
        return result
