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
import re
import pynos.device

class ConfigureVcenter(Action):
    """
    Implements the logic to add established Vcenter on the device.
       This action acheives the below functionality:
        1. Add vcenter
        2. Activate vcenter
    """
    def __init__(self, config=None):
        super(ConfigureVcenter, self).__init__(config=config)
        
    def run(self, host=None, username=None, password=None, vcenter_name=None, vcenter_url=None, vcenter_user=None, vcenter_pass=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['vip']
            
        if username is None:
            username = self.config['username']
            
        if password is None:
            password = self.config['password']
            
        if vcenter_name is None:
            vcenter_name = self.config['vcenter_name']
            
        if vcenter_user is None:
            vcenter_user = self.config['vcenter_user']
            
        if vcenter_pass is None:
            vcenter_pass = self.config['vcenter_pass']
            
        if vcenter_url is None:
            vcenter_url = self.config['vcenter_url']
        
        conn = (host, '22')
        auth = (username, password)
        
        changes = {}
        
        with pynos.device.Device(conn=conn, auth=auth) as device:
            changes['pre_requisites'] = self._check_requirements(device, vcenter_url)
            changes['configure_vcenter'] = False
            if changes['pre_requisites']:
                changes['configure_vcenter'] = self._configure_vcenter(device, vcenter_name, vcenter_user, vcenter_pass, vcenter_url)
            else:
                self.logger.info(
                    'Pre-requisites validation failed for vcenter configuration')

            if not changes['configure_vcenter']:
                self.logger.info(
                    'vcenter configuration Failed')
                exit(1)
            else:
                self.logger.info(
                    'closing connection to %s after configuring vcenter successfully!',host)
                return changes

    def _check_requirements(self, device, url):
        '''
        Verify if vcenter pre-exists
        '''
        #Logic to check if url is in the format: http(s)://<>
        pattern = re.compile(
            r'^(?:http)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'

            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip

            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not pattern.search(url):
            self.logger.info('Invalid URL')
            return False

        #Logic to check vcenter already exists.
        vc_list = device.vcenter.get_vcenter()
        for vc in vc_list:
            if vc['url'] == str(url):
                self.logger.info("Vcenter with url: %s already configured on the device" % url)
                return False
        return True

    def _configure_vcenter(self, device, vcenter_name, vcenter_user, vcenter_pass, vcenter_url ):
        result = self._create_vcenter(device, vcenter_name, vcenter_url, vcenter_user, vcenter_pass)
        if result:
            result = self._activate_vcenter(device, vcenter_name)
        return result

    def _create_vcenter(self, device, vcenter_name, vcenter_url, vcenter_user, vcenter_pass):
        """
        Create Vcenter on the device
        """
        try:
            device.vcenter.add_vcenter(id=vcenter_name, url=vcenter_url, username=vcenter_user, password=vcenter_pass)
            return True
        except Exception as e:
            self.logger.error('Vcenter configuration Failed with Exception: %s' %e)
            return False
        
    def _activate_vcenter(self, device, vcenter_name):
        """
        Activate Vcenter
        """
        try:
            device.vcenter.activate_vcenter(name=vcenter_name)
            return True
        except Exception as e:
            self.logger.error('Vcenter configuration Failed with Exception: %s' % e)
            return False

