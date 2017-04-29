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
import time
import socket
import pynos.device
from netmiko import ConnectHandler
from st2actions.runners.pythonrunner import Action

class ConfigureVcs(Action):
    """
       Implements the logic to VCS Fabric Creation
       This action achieves the below functionality
           1. VcsId and rbridgeID Validation.
           2. Validates if VCS Fabric pre-exists on the device.
           3. VCS fabric configuration.
    """
    def __init__(self, config=None):
        super(ConfigureVcs, self).__init__(config=config)
        self.logger = logging.getLogger(__name__)

    def run(self, host=None, username=None, password=None, vcs_id=None, rbridge_id=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['vip']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        if vcs_id is None:
            vcs_id = self.config['vcs_id']

        if rbridge_id is None:
            rbridge_id = self.config['rbridge_id1']

        conn = (host, '22')
        auth = (str(username), str(password))
        changes = {}
        
        dev = pynos.device.Device(conn=conn, auth=auth)

        changes['pre_requisites'] = self._check_requirements(dev, vcs_id, rbridge_id)
        changes['create_vcs'] = False
        if changes['pre_requisites']:
            changes['create_vcs'] = self._configure_vcs(vcs_id, rbridge_id, host, auth)
        else:
            self.logger.info('Pre-requisites validation failed for interface configuration.')
        if not changes['create_vcs']:
            self.logger.info('VCS Fabric configuration Failed on the device %s', host)
            exit(1)
        else:
            self.logger.info('closing connection to %s after successful VCS Fabric configuring',
                             host)
            return changes

    def _check_requirements(self, device, vcs_id, rbridge_id):
        """
        Verify if VCS Fabric pre-exists with multiple nodes.
        """
        if int(vcs_id) > 8192 or int(vcs_id) < 1:
            raise ValueError('VCS Id is Invalid. Not in <1-8192> range')
        if int(rbridge_id) > 239 or int(rbridge_id) < 1:
            raise ValueError(' Rbridge ID is Invalid. Not in <1-239> range')
        return True


    def _configure_vcs(self, vcs_id, rb_id, host, auth):
        """VCS Fabric Configuration
        """
        #
        self.logger.info("Creating VCS Fabric on the device: %r with vcsId:%r and rbridgeId: %r",
                         host, vcs_id, rb_id)
        cmd = "vcs vcsid %s set-rbridge-id %s", vcs_id, rb_id
        cmds = [cmd, 'y']
        print cmds
        result = self._execute_cmd(host, auth, cmds)
        print result
        return bool(result)

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
                cli_output[cmd] = (net_connect.send_command(cmd, expect_string='[y/n]'))
                self.logger.info('successfully executed cli %s', cmd)
            return True

        except RuntimeError as e:
            self.logger.error('Execution of command: %s Failed with Exception: %s', e, cmd)
            return False
        finally:
            if net_connect is not None:
                net_connect.disconnect()

    def _if_device_reboot(self, host):

        #Logic to check if device has rebooted.

        self.logger.info("Checking if the device is rebooted after VCS command execution")
        result = 0
        t_elapsed = 1
        while t_elapsed < 120:
            response = self._verify_ssh_connectivity(ip=host)
            if response == 0:
                t_elapsed += 5
                time.sleep(5)
            else:
                result = 1
                time.sleep(10)
                self.logger.info('Device is rebooted after VCS configuration.')
                break
        return result

    def _verify_ssh_connectivity(self, **kwargs):
        ip = kwargs.pop('ip')
        port = kwargs.pop('port', 22)
        response = None
        try:
            socket.setdefaulttimeout(5)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            response = s.connect_ex((ip, port))

            s.close()
            return response
        except:
            return response
