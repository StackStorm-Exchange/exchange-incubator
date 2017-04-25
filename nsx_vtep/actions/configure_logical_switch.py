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

from NSX.nsx import NSX
from st2actions.runners.pythonrunner import Action
import logging
import os

class configureLogicalSwitch(Action):
    def __init__(self, config=None, action_service=None):
        super(configureLogicalSwitch, self).__init__(config=config, action_service=action_service)
        
    def run(self, nsx_mgr_ip=None, nsx_mgr_user=None, nsx_mgr_pass=None, lswitch_name=None, vlan=None, port_name=None, switch_name=None, hardware_gateway_name=None):

        if nsx_mgr_ip is None:
            nsx_mgr_ip = self.config['nsx_mgr_ip']
            
        if nsx_mgr_user is None:
            nsx_mgr_user = self.config['nsx_mgr_user']
            
        if nsx_mgr_pass is None:
            nsx_mgr_pass = self.config['nsx_mgr_pass']
            
        if lswitch_name is None:
            lswitch_name = self.config['lswitch_name']
            
        if vlan is None:
            vlan = self.config['vlan']
            
        if port_name is None:
            port_name = self.config['port_name']
            
        if switch_name is None:
            switch_name = self.config['switch_name']
            
        if hardware_gateway_name is None:
            hardware_gateway_name = self.config['hardware_gateway_name']

        self.logger = logging.getLogger(__name__)

        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        file_path =  os.path.relpath("nsxraml/nsxvapi.raml")

        controller = NSX(raml_file=file_path, password=nsx_mgr_pass, username=nsx_mgr_user, ip=nsx_mgr_ip)
        changes = {}
        changes['pre_requisites'] = self._check_requirements(controller, lswitch_name, hardware_gateway_name)
        changes['configure_lswitch'] = False
        if changes['pre_requisites']:
            changes['configure_lswitch'] = self._configure_lswitch(controller,lswitch_name, vlan, port_name, switch_name, hardware_gateway_name)
        else:
            self.logger.info('Pre-requisites validation failed for lswitch configuration.')
        if changes['configure_lswitch']:
            self.logger.info(
                'closing connection to %s after configuring logical switch successfully!' % nsx_mgr_ip)
            return changes
        else:
            self.logger.info('Logical switch: %s configuration failed.' % lswitch_name)
            exit(1)

    def _check_requirements(self,controller, lswitch, hw_gw):
        '''
        Checks if hardware_gw and lswitch exists.
        '''

        #Logic to check of hw_gw is configured on the nsx-controller.
        print "validating hwgw"
        result = controller.get_hwdevice()
        gws = []
        if result is not None:
            gws = result['hardwareGateway']
        hwgw_present = False
        if isinstance(gws, dict):
            if gws['name'] == str(hw_gw):
                hwgw_present = True
        else:
            for gw in gws:
                if gw['name'] == str(hw_gw):
                    hwgw_present = True
                    break
        if not hwgw_present:
            self.logger.info('Hardware gateway: %s not present on the nsx-controller' %hw_gw)
            return False

        #Logic to check if the lswitch exists.
        print "validating lswitcgh"
        result = controller.get_logicalswitch()
        sw_list =[]
        if result is not None:
            sw_list = result['dataPage']['virtualWire']

        lswitch_present = False

        if isinstance(sw_list, dict):
            if sw_list['name'] == str(lswitch):
                lswitch_present = True
        else:
            for sw in sw_list:
                if sw['name'] == str(lswitch):
                    lswitch_present = True
                    break
        if  not lswitch_present:
            self.logger.info('Lswitch: %s is not present on the nsx-controller' %lswitch)
            return False
        return True

    def _configure_lswitch(self, controller, lswitch_name, vlan, port_name, switch_name, hardware_gateway_name):
        '''
        Logic to create the logical switch and attach hardware binding to it.
        '''
        #result = controller.create_logicalswitch(name=lswitch_name)
        print "create bidnign"
        result = controller.create_hardwarebinding(lswitch_name=lswitch_name, vlan=vlan, port_name=port_name,
                                              switch_name=switch_name, hardware_gateway_name=hardware_gateway_name)
        return result