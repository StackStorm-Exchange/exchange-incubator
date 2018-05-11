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
import re


class linkDomains(ACIBaseActions):
    def run (self, apic="default", data=None):
        self.set_connection(apic)
        post = {}

        for tnt in data:
            tenant = tnt
            for ap in data[tenant]:
                app_profile = ap
                for bd in data[tenant][app_profile]:
                    bridge_domain = bd
                    for eg in data[tenant][app_profile][bridge_domain]['epgs']:
                        epg = eg
                        current_domains = self.get_epg_domains(tenant, app_profile, epg)
                        for domain in data[tenant][app_profile][bridge_domain]['epgs'][epg]['domains']:

                            endpoint = "node/mo/uni/tn-%s/ap-%s/epg-%s.json" % (tenant, app_profile, epg)
                            payload = {}
                            payload['fvRsDomAtt'] = {} 
                            payload['fvRsDomAtt']['attributes'] = {}
                            payload['fvRsDomAtt']['attributes']['status'] = "created"
                            payload['fvRsDomAtt']['children'] = []

                            if "tdn" in self.config['apic'][apic]['domains'][domain].keys():
                                payload['fvRsDomAtt']['attributes']['tDn'] = self.config['apic'][apic]['domains'][domain]['tdn']
                            elif self.config['apic'][apic]['domains'][domain]['type'] == "phys":
                                apnum = re.match('.*?([0-9]+)$', app_profile).group(1)
                                payload['fvRsDomAtt']['attributes']['tDn'] =  ("uni/phys-Managed-Hosting-%s-Domain%s" % (tenant, apnum))
                            else:
                                raise Exception ("Incomplete Domain configuration")

                            if self.config['apic'][apic]['domains'][domain]['type'] == "vmm":
                                payload['fvRsDomAtt']['attributes']['resImedcy'] = "immediate"
                                vmmsecp = {}
                                vmmsecp['vmmSecP'] = {}
                                vmmsecp['vmmSecP']['attributes'] = {"status": "created"}
                                vmmsecp['vmmSecP']['children'] = []
                                payload['fvRsDomAtt']['children'].append(vmmsecp)
                                 
                            if payload['fvRsDomAtt']['attributes']['tDn'] not in current_domains:
                                post = self.aci_post(endpoint, payload)
                            else:
                                post[payload['fvRsDomAtt']['attributes']['tDn']] = "Already linked"

        return post
       
