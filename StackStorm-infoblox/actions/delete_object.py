from lib.action import InfobloxBaseAction

__all__ = [
    'DeleteObjectAction',
]

class DeleteObjectAction(InfobloxBaseAction):
    def run(self, ref, **kwargs):
        result = self.connection.delete_object(ref=ref)
        return result
