from lib.base import CrowdBaseAction


class CrowdAddUserAction(CrowdBaseAction):
    def run(self, username, password, email):
        data = {"password": password, "email": email}
        result = self.crowd.add_user(username, **data)

        return(bool(result), result)
