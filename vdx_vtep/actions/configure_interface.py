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

import re
import iptools
import pynos.device
from st2actions.runners.pythonrunner import Action

class ConfigureInterface(Action):
    """
       Implements the logic to configure interface
       This action acheives the below functionality
       1. Create/configure interface and assign IP to it
       2. Activate the interface
    """
    def __init__(self, config=None):
        super(ConfigureInterface, self).__init__(config=config)

    def run(self, host=None, mgmt_ip=None, username=None, password=None, intf_name=None, \
            intf_ip=None, intf_type=None, rbridge_id=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['vip']

        if mgmt_ip is None:
            mgmt_ip = self.config['mgmt_ip1']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        if intf_name is None:
            intf_name = self.config['intf_name']

        if intf_ip is None:
            intf_ip = self.config['intf_ip']

        if intf_type is None:
            intf_type = self.config['intf_type']

        if rbridge_id is None:
            rbridge_id = self.config['rbridge_id1']


        conn = (host, '22')
        validation_conn = (mgmt_ip, '22')
        auth = (username, password)

        changes = {}
        with pynos.device.Device(conn=conn, auth=auth) as device:
            validation_device = pynos.device.Device(conn=validation_conn, auth=auth)
            changes['pre_requisites'] = self._check_requirements(validation_device, \
                                            intf_type, intf_name, intf_ip, rbridge_id)
            changes['conf_intf'] = False
            if changes['pre_requisites']:
                changes['conf_intf'] = self._configure_interfacei(device, \
                                            intf_type, intf_name, intf_ip, rbridge_id)
            else:
                self.logger.info(
                    'Pre-requisites validation failed for interface configuration')
            if not changes['conf_intf']:
                self.logger.info(
                    'Interface %s %s configuration Failed' %(intf_type, intf_name))
                exit(1)
            else:
                self.logger.info(
                    'closing connection to %s after configuring interface %s %s successfully!' \
                    %(host, intf_type, intf_name))
                return changes

    def _check_requirements(self, device, intf_type, name, ip, rbridge_id):
        """ Verify if interface already configured.
        """

        if not self._validate_interface(intf_type, name, rbridge_id):
            raise ValueError('Invlaid %s Interface Id: %s' % (intf_type, name))

        if not self._validate_ip(ip):
            raise ValueError('Not a valid IP address %s', ip)

        # Logic to check if  interface already configured and active
        output = device.interface.interfaces
        is_interface_present = False
        for each_int in output:
            if each_int['interface-type'] == str(intf_type) and each_int['interface-name'] == str(name):
                is_interface_present = True
                break
        if is_interface_present:
            raise ValueError("Interface %s :%s already configured" % (intf_type, name))

        return True

    def _configure_interface(self, device, intf_type, name, ip, rbridge_id):
        result = self._set_interface_ip(device, intf_type, name, ip, rbridge_id)
        if result:
            result = self._set_interface_active(device, intf_type, name, rbridge_id)
        return result

    def _set_interface_ip(self, device, intf_type, name, ip, rbridge_id):
        try:
            device.interface.ip_address(int_type=intf_type, name=name, ip_addr=ip,
                                        rbridge_id=rbridge_id)
            return True
        except RuntimeError as e:
            self.logger.error(
                'Configuring IP for interface %s %s Failed with Exception: %s' \
                % (e, intf_type, name))
            return False

    def _set_interface_active(self, device, intf_type, name, rbridge_id):
        try:
            device.interface.admin_state(int_type=intf_type, name=name, enabled=True,
                                         rbridge_id=rbridge_id)
            return True
        except RuntimeError as e:
            self.logger.error(
                'Interface %s %s activation Failed with Exception: %s' % (e, intf_type, name))
            return False

    def _validate_interface(self, intf_type, intf_name, rbridge_id):
        msg = None
        # int_list = intf_name
        re_pattern1 = r"^(\d+)$"
        re_pattern2 = r"^(\d+)\/(\d+)\/(\d+)$"
        re_pattern3 = r"^(\d+)\/(\d+)$"
        intTypes = ["port_channel", "gigabitethernet", "tengigabitethernet", "fortygigabitethernet",
                    "hundredgigabitethernet", "ethernet"]
        NosIntTypes = ["gigabitethernet", "tengigabitethernet", "fortygigabitethernet"]
        if rbridge_id is None and 'loopback' in intf_type:
            msg = 'Must specify `rbridge_id` when specifying a `loopback`'
        elif rbridge_id is None and 've' in intf_type:
            msg = 'Must specify `rbridge_id` when specifying a `ve`'
        elif rbridge_id is not None and intf_type in intTypes:
            msg = 'Should not specify `rbridge_id` when specifying a ' + intf_type
        elif re.search(re_pattern1, intf_name):
            intf = intf_name
        elif re.search(re_pattern2, intf_name) and intf_type in NosIntTypes:
            intf = intf_name
        elif re.search(re_pattern3, intf_name) and 'ethernet' in intf_type:
            intf = intf_name
        else:
            msg = 'Invalid interface format'

        if msg is not None:
            self.logger.info(msg)
            return False

        intTypes = ["ve", "loopback", "ethernet"]
        if intf_type not in intTypes:
            tmp_vlan_id = pynos.utilities.valid_interface(intf_type, name=str(intf))

            if not tmp_vlan_id:
                self.logger.info("Not a valid interface type %s or name %s", intf_type, intf)
                return False

        return True

    def _validate_ip(self, ip):
        try:
            iptools.ipv4.validate_cidr(ip.decode('utf-8'))
            return True
        except ValueError:
            return False
        except AttributeError:
            return False
