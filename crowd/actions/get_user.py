from lib.base import CrowdBaseAction


class CrowdGetUserAction(CrowdBaseAction):
    def run(self, username):
        result = self.crowd.get_user(username)

        if result is None:
            return(bool(result), result)
        else:
            return(True, result)
