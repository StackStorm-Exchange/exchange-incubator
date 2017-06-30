import requests
from Tuleap.RestClient.Artifacts import Artifacts
from Tuleap.RestClient.Connection import CertificateVerification
from Tuleap.RestClient.Connection import Connection
from st2actions.runners.pythonrunner import Action


class CreateArtifacts(Action):
    def run(self, tracker_id, values_by_field_by_artifact):
        requests.packages.urllib3.disable_warnings()

        connection = Connection()
        response = None
        success = connection.login('https://'+self.config['tuleap_domain_name']+'/api/v1',
                                   self.config['tuleap_username'],
                                   self.config['tuleap_password'],
                                   CertificateVerification.Disabled)

        if success:
            # Artifacts
            artifacts = Artifacts(connection)

            for values_by_field in values_by_field_by_artifact.values():
                success = artifacts.create_artifact(tracker_id, values_by_field)

                if success:
                    response = artifacts.get_data()
                else:
                    return False, response

            return True, response

        return False, response
