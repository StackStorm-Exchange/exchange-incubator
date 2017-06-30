

import requests
from Tuleap.RestClient.Commons import Order
from Tuleap.RestClient.Connection import CertificateVerification
from Tuleap.RestClient.Connection import Connection
from Tuleap.RestClient.Projects import Projects
from st2actions.runners.pythonrunner import Action


class GetMilestones(Action):
    def run(self, project_id, order):
        requests.packages.urllib3.disable_warnings()

        connection = Connection()
        milestones = None
        success = connection.login('https://'+self.config['tuleap_domain_name']+'/api/v1',
                                   self.config['tuleap_username'],
                                   self.config['tuleap_password'],
                                   CertificateVerification.Disabled)

        if success:
            # Projects
            projects = Projects(connection)

            if order == 'descending':
                success = projects.request_milestones(project_id, Order.Descending)
            else:
                success = projects.request_milestones(project_id, Order.Ascending)

            if success:
                milestones = projects.get_data()

                return True, milestones

        return False, milestones
