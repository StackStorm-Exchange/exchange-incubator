from lib.action import InfobloxBaseAction

__all__ = [
    'CreateObjectAction',
]

class CreateObjectAction(InfobloxBaseAction):
    def run(self, object_type, **kwargs):
        result = self.connection.create_object(object_type, kwargs)
        return result
