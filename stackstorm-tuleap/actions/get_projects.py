from Tuleap.RestClient.Projects import Projects
from lib.base import BaseTuleapAction


class GetProjects(BaseTuleapAction):
    def run(self):
        success = self._login()
        if success:
            # Projects
            projects = Projects(self.connection)
            success = projects.request_project_list()
            if success:
                self.response = projects.get_data()

                return True, self.response

        return False, self.response
