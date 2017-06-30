from Tuleap.RestClient.Projects import Projects
from lib.base import BaseTuleapAction


class GetPlannings(BaseTuleapAction):
    def run(self, project_id):
        success = self._login()
        if success:
            # Projects
            projects = Projects(self.connection)
            success = projects.request_plannings(project_id)
            if success:
                self.response = projects.get_data()

                return True, self.response

        return False, self.response
