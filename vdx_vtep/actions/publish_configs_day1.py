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

class PublishConfigs(Action):
    def __init__(self, config=None):
        super(PublishConfigs, self).__init__(config=config)

    def run(self):
        configs = {}

        configs['vip'] = self.config['vip']
        configs['username'] = self.config['username']
        configs['password'] = self.config['password']
        configs['overlay_gateway_name'] = self.config['overlay_gateway_name']
        return configs
