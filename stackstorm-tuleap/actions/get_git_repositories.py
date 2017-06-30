from Tuleap.RestClient.Commons import GitFields
from Tuleap.RestClient.Projects import Projects
from lib.base import BaseTuleapAction


class GetGitRepositories(BaseTuleapAction):
    def run(self, project_id, git_fields):
        success = self._login()
        if success:
            # Projects
            projects = Projects(self.connection)
            if git_fields == 'all':
                success = projects.request_git(project_id, GitFields.All)
            else:
                success = projects.request_git(project_id, GitFields.Basic)
            if success:
                self.response = projects.get_data()

                return True, self.response

        return False, self.response
