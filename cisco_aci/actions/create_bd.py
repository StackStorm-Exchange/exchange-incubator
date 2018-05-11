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
        
        for tnt in data:
            tenant = tnt
            for ap in data[tenant]:
                app_profile = ap
                for bd in data[tenant][app_profile]:
                    bridge_domain = bd
                    bridge_domain_dn = "uni/tn-%s/BD-%s" % (tenant, bridge_domain)
                    all_bds = self.get_bd_list()
                    
                    if bridge_domain_dn in all_bds:
                        post[bridge_domain_dn] = {"status":"Bridge Domain already exists"}
                    else:
                        endpoint = "node/mo/uni/tn-%s/BD-%s.json" % (tenant, bridge_domain)

                        payload = {}
                        payload['fvBD'] = {}
                        payload['fvBD']['attributes'] = {}
                        for item in self.config['defaults']['BD']:
                            payload['fvBD']['attributes'][item] = self.config['defaults']['BD'][item]
                        payload['fvBD']['attributes']['dn'] = "uni/tn-%s/BD-%s" % (tenant, bridge_domain)
                        payload['fvBD']['attributes']['name'] = bridge_domain
                        payload['fvBD']['attributes']['rn'] = "BD-%s" % bridge_domain
                        payload['fvBD']['attributes']['status'] = "created"
                        payload['fvBD']['children'] = []

                        fsRsBd = {}
                        fsRsBd['fvRsCtx'] = {}
                        fsRsBd['fvRsCtx']['attributes'] = {}
                        if data[tenant][app_profile][bridge_domain]['vrf']:
                            fsRsBd['fvRsCtx']['attributes']['tnFvCtxName'] = data[tenant][app_profile][bridge_domain]['vrf']
                        else:
                            fsRsBd['fvRsCtx']['attributes']['tnFvCtxName'] = "%s-VRF1" % tenant
                        fsRsBd['fvRsCtx']['attributes']['status'] = "created,modified"
                        fsRsBd['fvRsCtx']['children'] = []
                        payload['fvBD']['children'].append(fsRsBd)
                        
                        post[bridge_domain_dn] = self.aci_post(endpoint, payload)
     
        return post
       
