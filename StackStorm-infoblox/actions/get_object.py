from lib.action import InfobloxBaseAction

__all__ = [
    'GetObjectAction',
]

class GetObjectAction(InfobloxBaseAction):
    def run(self, object_type, **kwargs):
        # remove null values as the API treats those as expected
        _keys = list(kwargs.keys())
        for k in _keys:
            if kwargs[k] is None:
                del kwargs[k]
        result = self.connection.get_object(
            object_type,
            payload=kwargs)
        return result
