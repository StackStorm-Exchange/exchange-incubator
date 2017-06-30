import requests
from Tuleap.RestClient.Commons import GitFields
from Tuleap.RestClient.Connection import CertificateVerification
from Tuleap.RestClient.Connection import Connection
from Tuleap.RestClient.Projects import Projects
from st2actions.runners.pythonrunner import Action


class GetGitRepositories(Action):
    def run(self, project_id, git_fields):
        requests.packages.urllib3.disable_warnings()

        connection = Connection()
        git_repositories = None
        success = connection.login('https://'+self.config['tuleap_domain_name']+'/api/v1',
                                   self.config['tuleap_username'],
                                   self.config['tuleap_password'],
                                   CertificateVerification.Disabled)

        if success:
            # Projects
            projects = Projects(connection)

            if git_fields == 'all':
                success = projects.request_git(project_id, GitFields.All)
            else:
                success = projects.request_git(project_id, GitFields.Basic)

            if success:
                git_repositories = projects.get_data()

                return True, git_repositories

        return False, git_repositories
