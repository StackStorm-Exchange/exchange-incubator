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

from lib.aci import ACIBaseActions


class createBD(ACIBaseActions):
    def run (self, apic="default", data=None):
        self.set_connection(apic)
        post = {}
        
        for tenant in data:
            for app_profile in data[tenant]:
                all_aps = self.get_ap_list()                
                app_profile_dn = "uni/tn-%s/ap-%s" % (tenant, app_profile)
                if app_profile_dn in all_aps:
                    post[app_profile_dn] = {"status":"Application Profile already exists"}
                else:
                    endpoint = "node/mo/%s.json" % (app_profile_dn)

                    payload = {}
                    payload['fvAp'] = {}
                    payload['fvAp']['attributes'] = {}
                    if self.config['defaults']:
                        if "AP" in self.config['defaults'].keys():
                            for item in self.config['defaults']['AP']:
                                payload['fvAp']['attributes'][item] = self.config['defaults']['AP'][item]
                    payload['fvAp']['attributes']['dn'] = app_profile_dn
                    payload['fvAp']['attributes']['name'] = app_profile
                    payload['fvAp']['attributes']['status'] = "created"
                    payload['fvAp']['children'] = []
                        
                    post[app_profile_dn] = self.aci_post(endpoint, payload)
     
        return post
       
