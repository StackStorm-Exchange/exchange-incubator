import requests
from Tuleap.RestClient.Connection import CertificateVerification
from Tuleap.RestClient.Connection import Connection
from Tuleap.RestClient.Trackers import Tracker
from st2actions.runners.pythonrunner import Action


class GetArtifacts(Action):
    def run(self, tracker_id):
        requests.packages.urllib3.disable_warnings()

        connection = Connection()
        artifact_list = None
        success = connection.login('https://'+self.config['tuleap_domain_name']+'/api/v1',
                                   self.config['tuleap_username'],
                                   self.config['tuleap_password'],
                                   CertificateVerification.Disabled)

        if success:
            # Tracker
            trackers = Tracker(connection)

            success = trackers.request_artifact_list(tracker_id)

            if success:
                artifact_list = trackers.get_data()

                return True, artifact_list

        return False, artifact_list
