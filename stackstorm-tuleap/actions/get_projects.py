import requests
from Tuleap.RestClient.Connection import CertificateVerification
from Tuleap.RestClient.Connection import Connection
from Tuleap.RestClient.Projects import Projects
from st2actions.runners.pythonrunner import Action


class GetProjects(Action):
    def run(self):
        requests.packages.urllib3.disable_warnings()

        connection = Connection()
        project_list = None
        success = connection.login('https://'+self.config['tuleap_domain_name']+'/api/v1',
                                   self.config['tuleap_username'],
                                   self.config['tuleap_password'],
                                   CertificateVerification.Disabled)

        if success:
            # Projects
            projects = Projects(connection)

            success = projects.request_project_list()

            if success:
                project_list = projects.get_data()

                return True, project_list

        return False, project_list