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

class getSwitchCertificate(Action):
    """
       Implements the logic to get the nsx-controller client certficate
       This action achieves the below functionality
           1. Reads client certificate
    """
    def __init__(self, config=None):
        super(getSwitchCertificate, self).__init__(config=config)
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
        changes['get_cert'] = self._get_client_certificate(host, auth)
        if not changes['get_cert']:
            self.logger.info('Nsx-controller client-certificate is not generated on the device: %s',
                             host)
            exit(1)
        else:
            self.logger.info('closing connection to %s after reading nsx-controller \
                              client-certificate successfully', host)
            return changes

    def _get_client_certificate(self, host, auth):
        '''
        Logic to read the client certificate
        Return: certificate
        '''
        cmd = ["terminal length 0", "show nsx-controller client-cert"]
        result = self._execute_cmd(host, auth, cmd)
        cert = result['show nsx-controller client-cert']
        print cert
        #certificate = '\n'.join(cert)
        #print certificate
        if 'BEGIN CERTIFICATE' not in cert:
            return False
        return cert

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
                print cli_output
            return cli_output

        except RuntimeError as e:
            self.logger.error('Execution of command Failed with Exception: %s', e)
            return False
        finally:
            if net_connect is not None:
                net_connect.disconnect()
