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

import pynos.device
from st2actions.runners.pythonrunner import Action
from ipaddress import ip_interface

class ConfigureVcsVip(Action):
    """
           Implements the logic to set Virtual IP in VCS Fabric.
           This action acheives the below functionality:
           1. Set VIP on the device
    """
    def __init__(self, config=None):
        super(ConfigureVcsVip, self).__init__(config=config)

    def run(self, host=None, vip_mask=None, username=None, password=None):
        """Run helper methods to implement the desired state.
        """
        if vip_mask is None:
            vip_mask = self.config['vip_mask']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        if host is None:
            host = self.config['mgmt_ip1']

        conn = (host, '22')
        auth = (username, password)

        changes = {}

        with pynos.device.Device(conn=conn, auth=auth) as device:
            changes['pre_requisites'] = self._check_requirements(device, vip_mask)
            changes['configure_vcs'] = False
            if changes['pre_requisites']:
                changes['configure_vcs'] = self._set_vcs_vip(device, vip_mask)
            else:
                self.logger.info(
                    'Pre-requisites validation failed for Virtual IP configuration')

            if not changes['configure_vcs']:
                self.logger.info('Virtual IP configuration in Vcs Fabric Failed')
                exit(1)
            else:
                self.logger.info(
                    'closing connection to %s after configuring Virtual IP successfully!',
                    host)
            return changes


    def _check_requirements(self, device, vip):
        """ Verify if the Virtual IP already exists
        """


        ipaddress = ip_interface(unicode(vip))
        vips = device.vcs.vcs_vip(get=True)

        if ipaddress.version == 4:
            ipv4_config = vips['ipv4_vip']
            conf = ipv4_config.data.find('.//{*}address')
        if ipaddress.version == 6:
            ipv6_config = vips['ipv6_vip']
            conf = ipv6_config.data.find('.//{*}ipv6address')

        if conf is not None:
            self.logger.info("VCS virtual IPv %s address is already configured" % ipaddress.version)
            return False
        return True

    def _set_vcs_vip(self, device, vip):
        """
         Set VCS Virtual IP on the device.
        """

        try:
            device.vcs.vcs_vip(vip=vip)
            return True
        except RuntimeError as e:
            self.logger.error(
                'Configuring VCS VIP: %s Failed with Exception: %s' % (e, vip))
            return False
