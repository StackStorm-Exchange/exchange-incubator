from lib.base import CrowdBaseAction


class CrowdSetAttributeAction(CrowdBaseAction):
    def run(self, username, attribute, value):
        result = self.crowd.set_user_attribute(username, attribute, value)

        return(bool(result), result)
