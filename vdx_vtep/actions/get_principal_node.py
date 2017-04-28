# Copyright 2017 Great Software Laboratory Pvt. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import pynos.device
from st2actions.runners.pythonrunner import Action
class getPrincipaldevice(Action):
    """
    Implements the logic to get the principal rbridge device.
    """
    def __init__(self, config=None):
        super(getPrincipaldevice, self).__init__(config=config)
        self.logger = logging.getLogger(__name__)
    def run(self, host, username, password):
        """
        Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['mgmt_ip1']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        conn = (host, '22')
        auth = (username, password)

        changes = {}
        with pynos.device.Device(conn=conn, auth=auth) as device:
            changes['get_principal_rb'] = self._get_principal_rb(device)
            if changes['get_principal_rb'] is None:
                self.logger.info('Failed to get the principal node')
                exit(1)
            else:
                return changes['get_principal_rb']

    def _get_principal_rb(self, device):
        """
        Get principal rbridge device in the VCS
        """
        try:
            result = device.vcs.vcs_nodes
            principal_node = None
            for node in result:
                if node['node-status'] == 'Co-ordinator':
                    principal_node = node['node-switch-ip']
                    break
            return principal_node
        except RuntimeError as e:
            self.logger.error('Failed to get the principal node with error: %s', e)
            return False
