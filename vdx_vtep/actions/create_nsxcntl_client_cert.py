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
from netmiko import ConnectHandler
from st2actions.runners.pythonrunner import Action

class createCertificate(Action):
    """
       Implements the logic to generate the nsx-controller client certficate
       This action achieves the below functionality
           1. Generates client certificate
    """
    def __init__(self, config=None):
        super(createCertificate, self).__init__(config=config)
        self.logger = logging.getLogger(__name__)

    def run(self, host=None, username=None, password=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['vip']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        auth = (str(username), str(password))

        changes = {}
        changes['create_cert'] = self._create_client_certificate(host, auth)
        if not changes['create_cert']:
            self.logger.info('Nsx-controller client-certificate already present on the device: %s',
                             host)
            exit(1)
        else:
            self.logger.info('closing connection to %s after generating nsx-controller \
                              client-certificate successfully', host)
            return changes

    def _create_client_certificate(self, host, auth):
        '''
        Logic to generate certificate.
        '''

        cmd = ["terminal length 0", "nsx-controller client-cert generate"]
        result = self._execute_cmd(host, auth, cmd)
        cert = result['nsx-controller client-cert generate']
        cert = ''.join(cert)
        if 'Certificate already present' in cert:
            return False
        return True

    def _execute_cmd(self, host, auth, cli_cmd):
        '''
        Logic to connect/ssh to the device and execute the command
        '''
        opt = {'device_type': 'brocade_vdx'}
        opt['ip'] = host
        opt['username'] = auth[0]
        opt['password'] = auth[1]
        opt['verbose'] = True
        opt['global_delay_factor'] = 0.5
        net_connect = None
        cli_output = {}
        try:
            net_connect = ConnectHandler(**opt)
            for cmd in cli_cmd:
                cmd = cmd.strip()
                cli_output[cmd] = (net_connect.send_command(cmd, expect_string='#'))
                self.logger.info('successfully executed cli %s', cmd)
            return cli_output
        except RuntimeError as e:
            self.logger.error('Execution of command: %s Failed with Exception: %s', e, cmd)
            return False
        finally:
            if net_connect is not None:
                net_connect.disconnect()
