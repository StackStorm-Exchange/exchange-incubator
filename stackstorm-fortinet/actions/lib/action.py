import pyfortiapi

from st2common import log as logging
from st2common.runners.base_action import Action

class FortinetBaseAction(Action):
    def __init__(self, config):
        super(FortinetBaseAction, self).__init__(config)
        self._firewall_ip = self.config['firewall_ip']
        self._username = self.config['username']
        self._password = self.config['password']
        self.device = self.fortinet_device()
    
    def fortinet_device(self):
        device = pyfortiapi.FortiGate(ipaddr=self._firewall_ip, username=self._username, password=self._password)
        return device

