from lib.base import CrowdBaseAction


class CrowdAddUserToGroupAction(CrowdBaseAction):
    def run(self, username, groupname):
        result = self.crowd.add_user_to_group(username, groupname)

        return(bool(result), result)
