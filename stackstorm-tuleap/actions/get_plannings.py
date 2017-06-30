import requests
from Tuleap.RestClient.Connection import CertificateVerification
from Tuleap.RestClient.Connection import Connection
from Tuleap.RestClient.Projects import Projects
from st2actions.runners.pythonrunner import Action


class GetPlannings(Action):
    def run(self, project_id):
        requests.packages.urllib3.disable_warnings()

        connection = Connection()
        plannings = None
        success = connection.login('https://' + self.config['tuleap_domain_name'] + '/api/v1',
                                   self.config['tuleap_username'],
                                   self.config['tuleap_password'],
                                   CertificateVerification.Disabled)

        if success:
            # Projects
            projects = Projects(connection)

            success = projects.request_plannings(project_id)

            if success:
                plannings = projects.get_data()

                return True, plannings

        return False, plannings
