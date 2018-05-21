from st2common.runners.base_action import Action

from checkpoint import CheckpointApi


class CheckpointBaseAction(Action):
    def __init__(self, config):
        super(CheckpointBaseAction, self).__init__(config)
        self._firewall_ip = self.config['firewall_ip']
        self._username = self.config['username']
        self._password = self.config['password']
        self.device = self.device()

    def device(self):
        device = CheckpointApi(checkpoint=self._firewall_ip, username=self._username,
                               password=self._password)

        return device
