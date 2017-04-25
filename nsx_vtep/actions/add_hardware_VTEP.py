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

class AddHardwareVtep(Action):
    def __init__(self, config=None, action_service=None):
        super(AddHardwareVtep, self).__init__(config=config, action_service=action_service)
        
    def run(self, nsx_mgr_ip=None, nsx_mgr_user=None, nsx_mgr_pass=None, vtep_name=None):
        if nsx_mgr_ip is None:
            nsx_mgr_ip = self.config['nsx_mgr_ip']
            
        if nsx_mgr_user is None:
            nsx_mgr_user = self.config['nsx_mgr_user']
            
        if nsx_mgr_pass is None:
            nsx_mgr_pass = self.config['nsx_mgr_pass']
            
        if vtep_name is None:
            vtep_name = self.config['vtep_name']
            
        self.controller = NSX(raml_file='/opt/stackstorm/packs/nsx/actions/nsxraml/nsxvapi.raml',password=nsx_mgr_pass, username=nsx_mgr_user, ip=nsx_mgr_ip)
        
        with open("/tmp/cert", "r") as f:
            cert = f.read()
        
        output = self._add_hw_vtep_cert(cert, vtep_name)
        
        return output
        
    def _add_hw_vtep_cert(self, cert, vtep_name):
        return self.controller.add_hwdevice_cert(cert=cert, name=vtep_name, bfd=True)
        