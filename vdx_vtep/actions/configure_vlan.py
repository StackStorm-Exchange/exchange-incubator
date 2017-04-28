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
import pynos.device
import pynos.utilities
from st2actions.runners.pythonrunner import Action

class CreateVlan(Action):
    def __init__(self, config=None):
        super(CreateVlan, self).__init__(config=config)

    def run(self, host=None, username=None, password=None, vlan=None, intf_desc=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['vip']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        if vlan is None:
            vlan = self.config['vlan']

        conn = (host, '22')
        auth = (username, password)

        changes = {}

        with pynos.device.Device(conn=conn, auth=auth) as device:
            self.logger.info('successfully connected to %s to create vlan', host)
            # Check is the user input for VLANS is correct
            vlan_list = self._check_requirements(vlan_id=vlan)
            # Check if the description is valid
            valid_desc = True
            if intf_desc:
                # if description is passed we validate that the length is good.
                valid_desc = self.check_int_description(intf_description=intf_desc)
            if vlan_list and valid_desc:
                changes['vm_vlan'] = self._configure_vlan(device, vlan_id=vlan_list,
                                                          intf_desc=intf_desc, host=host)
            else:
                raise ValueError('Input is not a valid vlan or description')
            self.logger.info('closing connection to %s after configuring create vlan -- all done!',
                             host)
        return changes

    def _check_requirements(self, vlan_id):
        """Fail the task if vlan id is zero or one or above 4096 .
        """

        re_pattern1 = r"^(\d+)$"
        re_pattern2 = r"^(\d+)\-?(\d+)$"

        if re.search(re_pattern1, vlan_id):
            try:
                vlan_id = (int(vlan_id),)
            except ValueError:
                self.logger.info("Could not convert data to an integer.")
                return None
        elif re.search(re_pattern2, vlan_id):
            try:
                vlan_id = re.match(re_pattern2, vlan_id)
            except ValueError:
                self.logger.info("Not in valid range format.")
                return None

            if int(vlan_id.groups()[0]) == int(vlan_id.groups()[1]):
                self.logger.warning("Use range command only for diff vlans")
            vlan_id = range(int(vlan_id.groups()[0]), int(vlan_id.groups()[1]) + 1)

        else:
            self.logger.info("Invalid vlan format")
            return None

        for vid in vlan_id:
            if vid > 4096:
                extended = "true"
            else:
                extended = "false"
            tmp_vlan_id = pynos.utilities.valid_vlan_id(vid, extended=extended)
            reserved_vlan_list = range(4087, 4096)
            reserved_vlan_list.append(1002)

            if not tmp_vlan_id:
                self.logger.info("'Not a valid VLAN %s", vid)
                return None
            if vid == 1:
                self.logger.info("vlan %s is default vlan", vid)
                return None
            elif vid in reserved_vlan_list:
                self.logger.info("Vlan cannot be created, as it is not a user/fcoe vlan %s", vid)
                return None

        return vlan_id

    def _configure_vlan(self, device, vlan_id, intf_desc, host):
        """Configure vlan under global mode.
        """

        vlan_len = len(vlan_id)
        sysvlans = device.interface.vlans
        is_vlan_interface_present = False

        #The below code is to verify the given vlan is already present in VDX switch
        vlan_list = []
        for vlan in vlan_id:
            for svlan in sysvlans:
                temp_vlan = int(svlan['vlan-id'])
                if temp_vlan == vlan:
                    is_vlan_interface_present = True
                    vlan_list.append(vlan)
                    self.logger.info('vlan %s already present on %s', vlan, host)
                    if intf_desc:
                        device.interface.description(int_type="vlan", name=vlan,
                                                     desc=intf_desc)
                    else:
                        self.logger.debug('Skipping description configuration')
                    if vlan_len == 1:
                        break

            #The below code is for creating single vlan.
            if not is_vlan_interface_present and vlan_len == 1:
                self.logger.info('configuring vlan %s on %s', vlan, host)
                error = device.interface.add_vlan_int(str(vlan))
                if intf_desc:
                    device.interface.description(int_type="vlan", name=vlan,
                                                 desc=intf_desc)
                else:
                    self.logger.debug('Skipping description configuration')
                if not error:
                    msg = 'Fabric is not enabled to support Virtual Fabric configuration \
                           on %s' % host
                    raise ValueError(msg)

        # The below code is for creating more than one vlan.
        if vlan_len > 1:
            vid_list = [x for x in vlan_id if x not in vlan_list]
            for vlan in vid_list:
                self.logger.info('configuring vlan %s on %s', vlan, host)
                error = device.interface.add_vlan_int(str(vlan))
                if intf_desc:
                    device.interface.description(int_type="vlan", name=vlan,
                                                 desc=intf_desc)
                else:
                    self.logger.debug('Skipping description configuration')

                if not error:
                    msg = 'Fabric is not enabled to support Virtual Fabric configuration \
                           on %s' % host
                    raise ValueError(msg)

        return True
