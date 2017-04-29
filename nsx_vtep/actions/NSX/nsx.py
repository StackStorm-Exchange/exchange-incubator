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

from nsxramlclient.client import NsxClient
import logging
class NSX():
    '''
    NSX Class: Following functionality are implemented.
    1. Create and get a hardware gateway.
    2. Create and get a hardware binding.
    3. Create and get a logical switch.
    '''

    def __init__(self,**kwargs):
        self._nsxraml_file = kwargs.pop('raml_file')
        self._nsx_password = kwargs.pop('password')
        self._nsx_username = kwargs.pop('username')
        self._nsxmanager = kwargs.pop('ip')
        self._client_session = NsxClient(self._nsxraml_file, self._nsxmanager, self._nsx_username, self._nsx_password)
        self.logger = logging.getLogger(__name__)

    def add_hwdevice_cert(self,**kwargs):

        self._cert = str(kwargs.pop('cert'))
        self._bfd = kwargs.pop('bfd',True)
        self._name = str(kwargs.pop('name'))


        self.logger.info ("Creating Hardware Device: %s"%self._name)
        hw_dict = self._client_session.extract_resource_body_example('vdnHardwareGateway', 'create')

        hw_dict['hardwareGatewaySpec']['name'] = self._name
        hw_dict['hardwareGatewaySpec']['certificate'] = self._cert
        hw_dict['hardwareGatewaySpec']['bfdEnabled'] = self._bfd

        hw = self._client_session.create('vdnHardwareGateway', request_body_dict=hw_dict)

        if 200 in hw.values():
            return True
        return False

    def get_hwdevice(self):
        self.logger.info ("Reading Hardware Gateway Certificates")
        hw = self._client_session.read('vdnHardwareGateway')

        if 200 in hw.values():
            return hw['body']['list']
        else:
            return False

    def get_hwgateway_biding(self,**kwargs):
        lswitch_name = str(kwargs.pop('lswitch_name'))
        self.logger.info ("Reading Hardware Bidings for the logical switch id: %r"%lswitch_name)


        objid = self.get_lswitch_objectId(lswitch_name=lswitch_name)
        if objid:
            hw_bindings = self._client_session.read('vdnHardwareBinding',uri_parameters={'virtualWireID': objid})
            if 200 in hw_bindings.values():
                return hw_bindings['body']['list']
            else:
                return False
        else:
            self.logger.info ("Logical Switch: %r entry not found"%lswitch_name)
            return False


    def get_hwdevice_objectId(self,**kwargs):
        hwdevice_name = str(kwargs.pop('hwdevice_name'))

        hwdevice = self.get_hwdevice()
        objid = None
        hw_list = hwdevice['hardwareGateway']
        if isinstance(hw_list, dict):
            if hw_list['name'] == hwdevice_name:
                objid = hw_list['objectId']
        else:
            for i in hw_list:
                if i['name'] == hwdevice_name:
                    objid = i['objectId']
                    break
        return objid

    def get_logicalswitch(self):

        self.logger.info ("Reading list of Logical Switches")
        lswitch = self._client_session.read('logicalSwitchesGlobal')
        if 200 in lswitch.values():
            return lswitch['body']['virtualWires']
        else:
            return False

    def create_logicalswitch(self,**kwargs):
        lswitch_name = str(kwargs.pop('name'))

        zone = str(kwargs.pop('zone','TZ1'))
        controlplan_mode = str(kwargs.pop('controlplan_mode','UNICAST_MODE'))
        tenant = str(kwargs.pop('tenant','vsphere.local'))

        self.logger.info ("Crating Logical Switch: %r"%lswitch_name)


        # find the objectId of the Scope with the name of the Transport Zone
        vdn_scopes = self._client_session.read('vdnScopes', 'read')['body']
        vdn_scope_dict_list = [scope_dict for scope_dict in vdn_scopes['vdnScopes'].items()]
        vdn_scope = [scope[1]['objectId'] for scope in vdn_scope_dict_list if scope[1]['name'] == zone][0]

        # get a template dict for the lswitch create
        lswitch_create_dict = self._client_session.extract_resource_body_example('logicalSwitches', 'create')
        #self._client_session.view_body_dict(lswitch_create_dict)

        # fill the details for the new lswitch in the body dict
        lswitch_create_dict['virtualWireCreateSpec']['controlPlaneMode'] = controlplan_mode
        lswitch_create_dict['virtualWireCreateSpec']['name'] = lswitch_name
        lswitch_create_dict['virtualWireCreateSpec']['tenantId'] = tenant

        # create new lswitch
        new_ls = self._client_session.create('logicalSwitches', uri_parameters={'scopeId': vdn_scope},request_body_dict=lswitch_create_dict)
        #self._client_session.view_response(new_ls)

        if 200 in new_ls.values():
            return True
        else:
            return False

    def get_lswitch_objectId(self,**kwargs):
        lswitch_name = str(kwargs.pop('lswitch_name'))

        lswitch = self.get_logicalswitch()
        objid = None
        sw_list = lswitch['dataPage']['virtualWire']
        if isinstance(sw_list,dict):
            if sw_list['name'] == lswitch_name:
                objid = sw_list['objectId']
        else:
            for i in sw_list:
                if i['name'] == lswitch_name:
                    objid = i['objectId']
                    break
        return objid

    def create_hardwarebinding(self,**kwargs):

        lswitch_name = str(kwargs.pop('lswitch_name'))
        vlan = str(kwargs.pop('vlan'))
        port_name = str(kwargs.pop('port_name'))
        switch_name = str(kwargs.pop('switch_name'))
        hardware_gateway_name = str(kwargs.pop('hardware_gateway_name'))

        self.logger.info ("Creating Hardware bindings for the logical switch: %r"%lswitch_name)
        hwdevice_id = self.get_hwdevice_objectId(hwdevice_name=hardware_gateway_name)
        if not hwdevice_id:
            self.logger.info ("Hardware device entry: %r entry not found" % hardware_gateway_name)
            return False
        objectId = self.get_lswitch_objectId(lswitch_name=lswitch_name)
        if objectId :
            hw_dict = self._client_session.extract_resource_body_example('vdnHardwareBinding', 'create')
            hw_dict['hardwareGatewayBinding']['hardwareGatewayId'] = hwdevice_id
            hw_dict['hardwareGatewayBinding']['portName'] = port_name
            hw_dict['hardwareGatewayBinding']['vlan'] = vlan
            hw_dict['hardwareGatewayBinding']['switchName'] = switch_name

            hw = self._client_session.create('vdnHardwareBinding', uri_parameters={'virtualWireID': objectId},
                                   request_body_dict=hw_dict)

            if 200 in hw.values():
                return True
            else:
                return False

        else:
            self.logger.info ("Logical Switch: %r entry not found" % lswitch_name)
            return False
