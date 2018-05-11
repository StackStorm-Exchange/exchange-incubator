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

class createEPG(ACIBaseActions):
    def run (self, apic="default", data=None):
        self.set_connection(apic)
        post = {}
        all_bds = self.get_bd_list()
        all_epgs = self.get_epg_list()

        for tnt in data:
            tenant = tnt
            for ap in data[tenant]:
                app_profile = ap
                for bd in data[tenant][app_profile]:
                    bridge_domain = bd
                    bridge_domain_dn = "uni/tn-%s/BD-%s" % (tenant, bridge_domain)
                    
                    if bridge_domain_dn not in all_bds:
                        raise Exception("Unable to find Bridge Domain")

                    for eg in data[tenant][app_profile][bridge_domain]['epgs']:
                        payload = {}
                        epg = eg
                        dn = "uni/tn-%s/ap-%s/epg-%s" % (tenant, app_profile, epg)
                        if dn in all_epgs:
                            post[dn] = {"status": "EPG Already exists"}
                        else:
                            endpoint = "node/mo/uni/tn-%s/ap-%s/epg-%s.json" % (tenant, app_profile, epg)
                            payload['fvAEPg'] = {}
                            payload['fvAEPg']['attributes'] = {}
                            payload['fvAEPg']['attributes']['dn'] = dn
                            payload['fvAEPg']['attributes']['name'] = eg
                            payload['fvAEPg']['attributes']['rn'] = "epg-%s" % eg
                            payload['fvAEPg']['attributes']['status'] = "created"
                            payload['fvAEPg']['attributes']['descr'] = data[tenant][app_profile][bridge_domain]['epgs'][eg]['desc']
                            payload['fvAEPg']['children'] = []
                            fsRsBd = {}
                            fsRsBd['fvRsBd'] = {}
                            fsRsBd['fvRsBd']['attributes'] = {}
                            fsRsBd['fvRsBd']['attributes']['tnFvBDName'] = bridge_domain
                            fsRsBd['fvRsBd']['attributes']['status'] = "created,modified"
                            fsRsBd['fvRsBd']['children'] = []
                            payload['fvAEPg']['children'].append(fsRsBd)
                        
                            post[dn] = self.aci_post(endpoint, payload)
     
        return post
       
