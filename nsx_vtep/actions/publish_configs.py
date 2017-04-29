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

class AddHardwareVtep(Action):
    def __init__(self, config=None, action_service=None):
        super(AddHardwareVtep, self).__init__(config=config, action_service=action_service)

    def run(self):
        configs = {}

        configs['lswitch_name'] = self.config['lswitch_name']
        configs['nsx_mgr_ip'] = self.config['nsx_mgr_ip']
        configs['nsx_mgr_pass'] = self.config['nsx_mgr_pass']
        configs['nsx_mgr_user'] = self.config['nsx_mgr_user']
        configs['port_name'] = self.config['port_name']
        configs['switch_name'] = self.config['switch_name']
        configs['vlan'] = self.config['vlan']
        configs['vtep_name'] = self.config['vtep_name']

        return configs
