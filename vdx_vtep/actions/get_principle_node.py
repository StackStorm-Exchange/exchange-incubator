import logging
import pynos.device
from st2actions.runners.pythonrunner import Action
class getPrincipledevice(Action):
    """
       Implements the logic to get the principle rbridge device.
    """

    def run(self, host, username, password):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['mgmt_ip1']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        conn = (host, '22')
        auth = (username, password)
        self.logger = logging.getLogger(__name__)
        changes = {}
        with pynos.device.Device(conn=conn, auth=auth) as device:
            changes['get_principle_rb'] = self._get_principle_rb(device)
            if changes['get_principle_rb'] is None:
                self.logger.info('Failed to get the principle node')
                exit(1)
            else:
                return changes['get_principle_rb']

    def _get_principle_rb(self, device):
        """
        Get principle rbridge device in the VCS
        """
        try:
            result = device.vcs.vcs_nodes
            principal_node = None
            for node in result:
                if node['node-status'] == 'Co-ordinator':
                    principal_node = node['node-switch-ip']
                    break
            return principal_node
        except Exception as e:
            self.logger.error(
                'Failed to get the principle node with error: %s' %e)
            return False