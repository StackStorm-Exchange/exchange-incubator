from lib.base import CrowdBaseAction


class CrowdGetGroupsAction(CrowdBaseAction):
    def run(self, username):
        result = self.crowd.get_groups(username)

        if result is None:
            return(bool(result), result)
        else:
            return(True, result)
