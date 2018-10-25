from lib.base import CrowdBaseAction


class CrowdSetActiveAction(CrowdBaseAction):
    def run(self, username, active_state):
        result = self.crowd.set_active(username, active_state)

        return(bool(result), result)
