from st2common.runners.base_action import Action
from cohesity_management_sdk.cohesity_client import CohesityClient


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.client = self._get_client()

    def _get_client(self):
        hostname = self.config['hostname']
        username = self.config['username']
        password = self.config['password']
        domain = self.config['domain']
        return CohesityClient(hostname, username, password, domain)
