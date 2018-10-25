from lib.base import CrowdBaseAction


class CrowdCheckUserAction(CrowdBaseAction):
    def run(self, username):
        # Return True if the user exists in the Crowd application.
        result = self.crowd.user_exists(username)

        return(bool(result), result)
