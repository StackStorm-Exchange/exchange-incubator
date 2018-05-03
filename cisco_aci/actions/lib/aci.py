
# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json

from st2actions.runners.pythonrunner import Action


class ACIBaseActions(Action):

    def __init__(self, config):
        super(ACIBaseActions, self).__init__(config)
        if config is None:
            raise ValueError("No Configuration details found")

        if "apic" in config:
            if config['apic'] is None:
                raise ValueError("No apics defined")
            else:
                pass
        else:
            raise ValueError("No configuration details found")

        return

    def set_connection(self, apic=None):

        if apic == None:
            apic = "default"
        self.apic_address = self.config['apic'][apic]['address']
        self.apic_user = self.config['apic'][apic]['user']
        self.apic_passwd = self.config['apic'][apic]['passwd']
        self.apic_token = ""

        return

    def get_sessionid(self):
        url = 'https://%s/api/aaaLogin.json' % self.apic_address
        #url = 'https://%s/api/aaaLogin.json?gui-token-request=yes' % self.apic_address
        headers = {'Accept': 'application/json',
                   'Content-type': 'application/json'}
        payload = {}
        payload['aaaUser'] = {}
        payload['aaaUser']['attributes'] = {}
        payload['aaaUser']['attributes']['name'] = self.apic_user
        payload['aaaUser']['attributes']['pwd'] = self.apic_passwd

        p = requests.post(url, headers=headers, json=payload, verify=False)
        jdata = p.json()
        self.apic_token =  {'APIC-Cookie': jdata['imdata'][0]['aaaLogin']['attributes']['token']}

        return jdata
        #return self.apic_token

    def get_tenants(self):
        tenants = {}
        url = 'http://%s/api/node/class/fvTenant.json' % (self.apic_address)
        headers = {'Accept': 'application/json'}

        p = requests.get(url, headers=headers, verify=False, cookies=self.apic_token)
        jdata = p.json()
        return jdata


        return tenants


