import requests
from st2actions.runners.pythonrunner import Action
from Tuleap.RestClient.Connection import CertificateVerification
from Tuleap.RestClient.Connection import Connection

__all__ = [
    'BaseTuleapAction'
]


class BaseTuleapAction(Action):

    def __init__(self, config):
        super(BaseTuleapAction, self).__init__(config=config)
        requests.packages.urllib3.disable_warnings()
        self.response = None
        self.connection = Connection()

    def _login(self):
        return self.connection.login('https://' + self.config['tuleap_domain_name'] + '/api/v1',
                                     self.config['tuleap_username'],
                                     self.config['tuleap_password'],
                                     CertificateVerification.Disabled)
