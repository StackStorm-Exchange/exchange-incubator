
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
        if apic not in self.config['apic']:
            raise ValueError("Invalid apic")
        else:
            self.apic_address = self.config['apic'][apic]['address']
            self.apic_user = self.config['apic'][apic]['user']
            self.apic_passwd = self.config['apic'][apic]['passwd']
            self.apic_token = ""

        return self.get_sessionid()

    def get_sessionid(self):
        endpoint = 'aaaLogin.json' 
        payload = {}
        payload['aaaUser'] = {}
        payload['aaaUser']['attributes'] = {}
        payload['aaaUser']['attributes']['name'] = self.apic_user
        payload['aaaUser']['attributes']['pwd'] = self.apic_passwd

        jdata = self.aci_post(endpoint, payload)
        self.apic_token =  {'APIC-Cookie': jdata['imdata'][0]['aaaLogin']['attributes']['token']}

        return self.apic_token

    def get_tenants(self):
        tenants = {}
        endpoint = 'node/class/fvTenant.json'
        return self.aci_get(endpoint)

    def get_vrfs(self):
        tenants = {}
        endpoint = 'node/class/fvCtx.json'
        return self.aci_get(endpoint)

    def get_bds(self):
        tenants = {}
        endpoint = 'node/class/fvBD.json'
        return self.aci_get(endpoint)

    def get_bd_list(self):
        all_bds = []
        bds = self.get_bds()
        for item in bds['imdata']:
            all_bds.append(item['fvBD']['attributes']['dn'])
        return all_bds

    def get_aps(self):
        endpoint = 'node/class/fvAp.json'
        return self.aci_get(endpoint)

    def get_ap_list(self):
        all_aps = []
        aps = self.get_aps()
        for item in aps['imdata']:
            all_aps.append(item['fvAp']['attributes']['dn'])
        return all_aps
        
    def get_epgs(self):
        endpoint = 'node/class/fvAEPg.json'
        return self.aci_get(endpoint)

    def get_epg_list(self):
        epg_list = []
        epgs = self.get_epgs()
        for item in epgs['imdata']:
            epg_list.append(item['fvAEPg']['attributes']['dn'])
        return epg_list

    def get_static_bindings(self, tenant=None, app_profile=None):
        final_sb = {}
        final_sb['imdata'] = []
        dn_match = ""
        endpoint = 'node/class/fvRsPathAtt.json'
        sb_results = self.aci_get(endpoint)
        if tenant:
            dn_match = ("uni/tn-"+tenant)
            if app_profile:
                dn_match += ("/ap-"+app_profile)
           
            for item in sb_results['imdata']:
                if item['fvRsPathAtt']['attributes']['dn'].startswith(dn_match): 
                    final_sb['imdata'].append(item)
        else:
            final_sb = sb_results
        return final_sb 


    def get_domains(self):
        endpoint = 'node/class/fvDom.json'
        return self.aci_get(endpoint)

    def get_epg_domains(self, tenant, ap, epg):
        domains = []
        endpoint = "node/mo/uni/tn-%s/ap-%s/epg-%s.json?query-target=children&target-subtree-class=fvRsDomAtt" % (tenant, ap, epg)
        jdata = self.aci_get(endpoint)
        for entry in jdata['imdata']:
            domains.append(entry['fvRsDomAtt']['attributes']['tDn'])
        return domains

    def aci_get(self, endpoint):
        url = 'https://%s/api/%s' % (self.apic_address, endpoint)
        headers = {'Accept': 'application/json'}
        p = requests.get(url, headers=headers, verify=False, cookies=self.apic_token)
        return p.json()

    def aci_post(self, endpoint, payload):
        url = 'https://%s/api/%s' % (self.apic_address, endpoint)
        headers = {'Accept': 'application/json',
                   'Content-type': 'application/json'}
        try:
            p = requests.post(url, headers=headers, json=payload, cookies=self.apic_token, verify=False)
            p.raise_for_status()
            jdata = p.json()
        except requests.exceptions.HTTPError as e:
            raise Exception("Error: %s" % (p.json()['imdata'][0]['error']['attributes']['text']))

        return p.json()

