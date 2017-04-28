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
import pynos.device
import pynos.utilities
from st2actions.runners.pythonrunner import Action

class attachVlanToGw(Action):
    def __init__(self, config=None):
        Action.__init__(self, config=config)
        self.logger = logging.getLogger(__name__)

    def run(self, host=None, username=None, password=None, overlay_gateway_name=None, vlan=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['vip']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        if overlay_gateway_name is None:
            overlay_gateway_name = self.config['overlay_gateway_name']

        if vlan is None:
            vlan = self.config['vlan']

        conn = (host, '22')
        auth = (str(username), str(password))
        changes = {}

        self.logger = logging.getLogger(__name__)
        dev = pynos.device.Device(conn=conn, auth=auth)

        changes['pre_requisites'] = self._check_requirements(dev, overlay_gateway_name, vlan)
        changes['attach_vlan'] = False
        if changes['pre_requisites']:
            changes['attach_vlan'] = self._attach_vlan(host, auth, overlay_gateway_name, vlan)
        else:
            self.logger.info('Pre-requisites validation failed while attaching VLAN \
                to overlay gateway')
        if not changes['attach_vlan']:
            self.logger.info('Attach VLAN to overlay gateway has failed.')
            exit(1)
        else:
            self.logger.info('closing connection to %s after attaching VLAN \
                to overlay gateway', host)
            return changes

    def _check_requirements(self, dev, overlay_gateway_name, vlan):
        if not pynos.utilities.valid_vlan_id(vlan):
            raise ValueError("VlandId %s must be between `1` and `8191`" % vlan)

        # Logic to check if vlan is precreated
        is_vlan_exist = False
        output = dev.interface.vlans
        for each_vlan in output:
            if 'vlan-id' in each_vlan and each_vlan['vlan-id'] == str(vlan):
                is_vlan_exist = True
        if not is_vlan_exist:
            raise ValueError("VlanId %s does not exists" % vlan)

        # logic to check if overlay-Gateway is already present and vlan is already attached.
        result = dev.hw_vtep.get_overlay_gateway()
        if not result:
            self.logger.info(' No Overlay-Gateway configured on the device')
            return False
        else:
            if result['name'] == str(overlay_gateway_name):
                if 'attached-vlan' in result:
                    if str(vlan) in result['attached-vlan']:
                        self.logger.info('VLAN: %s is already attached to overlay gateway.', vlan)
                        return False
            else:
                self.logger.info('Overlay gateway: %s not configured on the switch.', \
                    overlay_gateway_name)
                return False
        return True


    def _attach_vlan(self, host, auth, overlay_gateway_name, vlan):
        '''
        Add Vlans to the overlay-gateway
        '''
        cmd1 = "overlay-gateway %s" % (overlay_gateway_name)
        cmd2 = "attach vlan %d" % (int(vlan))
        cmds = ['configure', cmd1, cmd2]
        return bool(self._execute_cmd(host, auth, cmds))

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
                cli_output[cmd] = (net_connect.send_command(cmd, expect_string='config'))
                self.logger.info('successfully executed cli %s', cmd)
            return True

        except RuntimeError as e:
            self.logger.error('Execution of command: %s Failed with Exception: %s', e, cmd)
            return False
        finally:
            if net_connect is not None:
                net_connect.disconnect()
