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

from st2actions.runners.pythonrunner import Action
import pynos.device
import iptools

class ConfigureNsxController(Action):
    """
       Implements the logic to configure NSX controller in VCS fabric.
       This action acheives the below functionality:
        1. Set nsx-controller name,ip and port
        2. Activate nsx-controller

    """
    def __init__(self, config=None):
        super(ConfigureNsxController, self).__init__(config=config)

    def run(self, host=None, username=None, password=None, nsx_cnt_name=None, nsx_cnt_ip=None, nsx_cnt_port=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host=self.config['vip']

        if username is None:
            username=self.config['username']

        if password is None:
            password=self.config['password']

        if nsx_cnt_name is None:
            nsx_cnt_name=self.config['nsx_cnt_name']
            
        if nsx_cnt_ip is None:
            nsx_cnt_ip=self.config['nsx_cnt_ip']
            
        if nsx_cnt_port is None:
            nsx_cnt_port=self.config['nsx_cnt_port']

        conn = (host, '22')
        auth = (username, password)

        changes = {}
        with pynos.device.Device(conn=conn, auth=auth) as device:
            changes['pre_requisites'] = self._check_requirements(device,nsx_cnt_ip)
            if changes['pre_requisites']:
                changes['configure_nsxcontroller'] = self._configure_nsx_controller(device, nsx_cnt_name, nsx_cnt_ip, nsx_cnt_port)
            else:
                changes['configure_nsxcontroller'] = False
                self.logger.info(
                    'Pre-requisites validation failed for nsx-controller configuration')
        if not changes['configure_nsxcontroller']:
            self.logger.info(
                'Nsx-controller configuration Failed')
            exit(1)
        else:
            self.logger.info(
                'closing connection to %s after configuring nsx-controller successfully!',
                host)
            return changes



    def _configure_nsx_controller(self,device, nsx_cnt_name, nsx_cnt_ip, nsx_cnt_port):
        """
        Configure nsx-controller on the device.
        """


        result = self._set_nsxcontroller_name(device, nsx_cnt_name)
        if result:
            result  = self._set_nsxcontroller_ip(device, nsx_cnt_name, nsx_cnt_ip)
        if result:
            result = self._set_nsxcontroller_port(device, nsx_cnt_name, nsx_cnt_port)
        if result:
            result = self._activate_nsxcontroller(device, nsx_cnt_name)
        return result

    def _check_requirements(self,device,ip):
        """ Verify if the nsx-controller already exists """

        if not self._validate_ip(ip):
            raise ValueError('Not a valid IP address %s', ip)
        if device.nsx.get_nsx_controller():
            self.logger.info(
                'NSX controller already configured on the device')
            result = False
        else:
            result = True
        return result

    def _set_nsxcontroller_name(self, device, nsx_cnt_name):
        """set NSX controller name.
        """
        try:
            device.nsx.nsx_controller_name(name=nsx_cnt_name)
            return True
        except Exception as e:
            self.logger.error(
                'Configuring NSX-Controller %s Failed with Exception: %s' % e)
            return False
        
    def _set_nsxcontroller_ip(self, device, nsx_cnt_name, nsx_cnt_ip):
        """set NSX controller IP.
        """
        try:
            device.nsx.set_nsxcontroller_ip(name=nsx_cnt_name, ip_addr=nsx_cnt_ip)
            return True
        except Exception as e:
            self.logger.error(
                'Configuring NSX-Controller %s Failed with Exception: %s' % e)
            return False
        
    def _set_nsxcontroller_port(self, device, nsx_cnt_name, nsx_cnt_port):
        """set NSX controller port.
        """
        try:
            device.nsx.set_nsxcontroller_port(name=nsx_cnt_name, port=nsx_cnt_port)
            return True
        except Exception as e:
            self.logger.error(
                'Configuring NSX-Controller %s Failed with Exception: %s' % e)
            return False
    
    def _activate_nsxcontroller(self, device, nsx_cnt_name):
        """activate NSX controller.
        """
        try:
            device.nsx.activate_nsxcontroller(name=nsx_cnt_name)
            return True
        except Exception as e:
            self.logger.error(
                'Configuring NSX-Controller %s Failed with Exception: %s' % e)
            return False
            
    def _validate_ip(self, ip):
        try:
            iptools.ipv4.validate_ip(ip.decode('utf-8'))
            return True
        except ValueError:
            return False
        except AttributeError:
            return False