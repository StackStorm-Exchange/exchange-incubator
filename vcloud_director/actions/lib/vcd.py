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
import xmltodict
from requests.auth import HTTPBasicAuth
from st2actions.runners.pythonrunner import Action


class VCDBaseActions(Action):

    def __init__(self, config):
        super(VCDBaseActions, self).__init__(config)
        if config is None:
            raise ValueError("No Configuration details found")

        if "vcloud" in config:
            if config['vcloud'] is None:
                raise ValueError("'vcloud' config defined by empty")
            else:
                pass
        else:
            raise ValueError("No Connection configuration details found")

    def set_connection(self, vcloud=None):
        if vcloud == None:
            vcloud = "default"

        self.vcd_host = self.config['vcloud'][vcloud]['host']
        self.vcd_user = self.config['vcloud'][vcloud]['user']
        self.vcd_pass = self.config['vcloud'][vcloud]['passwd']

    def get_sessionid(self):
        url = 'https://%s/api/sessions' % self.vcd_host
        headers = {'Accept': 'application/*+xml;version=5.1'
                  }
        p = requests.post(url, headers=headers, auth=(self.vcd_user+'@SYSTEM',self.vcd_pass), verify=False)
        self.vcd_auth =  p.headers['x-vcloud-authorization']

        return self.vcd_auth

    def get_pvdc_details(self, pvdc_ref):
        pvdc_data = {}
        pvdc_data['external_networks'] = {}
        pvdc_data['compute_capacity'] = {}
        pvdc_data['compute_capacity']['cpu'] = {}
        pvdc_data['compute_capacity']['memory'] = {}
        pvdc_data['network_pools'] = {}
        pvdc_data['storage_profiles'] = {}
        pvdc_data['hosts'] = {}
        
        url = 'https://%s/api/admin/extension/providervdc/%s' % (self.vcd_host,pvdc_ref)
        headers = {'Accept': 'application/*+xml;version=5.1',
                   'x-vcloud-authorization': self.vcd_auth
                  }
        p = requests.get(url, headers=headers, verify=False)
        jdata = xmltodict.parse(p.text)
        
        pvdc_data['id'] = jdata['vmext:VMWProviderVdc']['@id'].split('providervdc:', 1)[-1]
        pvdc_data['enabled'] = jdata['vmext:VMWProviderVdc']['vcloud:IsEnabled']

        for item in jdata['vmext:VMWProviderVdc']['vcloud:AvailableNetworks']['vcloud:Network']:
            pvdc_data['external_networks'][item['@name']] = {}
            pvdc_data['external_networks'][item['@name']]['id'] = item['@href'].split('externalnet/', 1)[-1]

        for item in jdata['vmext:VMWProviderVdc']['vcloud:ComputeCapacity']['vcloud:Cpu']:
            pvdc_data['compute_capacity']['cpu'][str(item).split('vcloud:', 1)[-1]] = jdata['vmext:VMWProviderVdc']['vcloud:ComputeCapacity']['vcloud:Cpu'][item]

        for item in jdata['vmext:VMWProviderVdc']['vcloud:ComputeCapacity']['vcloud:Memory']:
            pvdc_data['compute_capacity']['memory'][str(item).split('vcloud:', 1)[-1]] = jdata['vmext:VMWProviderVdc']['vcloud:ComputeCapacity']['vcloud:Memory'][item]

        for item in jdata['vmext:VMWProviderVdc']['vcloud:StorageProfiles']['vcloud:ProviderVdcStorageProfile']:
            pvdc_data['storage_profiles'][item['@name']] = {}
            pvdc_data['storage_profiles'][item['@name']]['id'] = item['@href'].split('pvdcStorageProfile/', 1)[-1]

        for item in jdata['vmext:VMWProviderVdc']['vmext:HostReferences']['vmext:HostReference']:
            pvdc_data['hosts'][item['@name']] = {}
            pvdc_data['hosts'][item['@name']]['id'] = item['@href'].split('host/', 1)[-1]

        if jdata['vmext:VMWProviderVdc']['vcloud:NetworkPoolReferences'] is not None:
            if isinstance (jdata['vmext:VMWProviderVdc']['vcloud:NetworkPoolReferences']['vcloud:NetworkPoolReference'], list):
                for item in jdata['vmext:VMWProviderVdc']['vcloud:NetworkPoolReferences']['vcloud:NetworkPoolReference']:
                    pvdc_data['network_pools'][item['@name']] = {}
                    pvdc_data['network_pools'][item['@name']]['id'] = item['@href'].split('networkPool/', 1)[-1]
            else:
                name = jdata['vmext:VMWProviderVdc']['vcloud:NetworkPoolReferences']['vcloud:NetworkPoolReference']['@name']
                nid = jdata['vmext:VMWProviderVdc']['vcloud:NetworkPoolReferences']['vcloud:NetworkPoolReference']['@href'].split('networkPool/', 1)[-1]
                pvdc_data['network_pools'][name] = {}
                pvdc_data['network_pools'][name]['id'] = nid

        return pvdc_data

    def get_pvdcs(self):
        url = 'https://%s/api/admin/extension/providerVdcReferences' % self.vcd_host
        headers = {'Accept': 'application/*+xml;version=5.1',
                   'x-vcloud-authorization': self.vcd_auth
                  }
        p = requests.get(url, headers=headers, verify=False)
        jdata = xmltodict.parse(p.text)
        jpvdcs = {}
        for pvdc in jdata['vmext:VMWProviderVdcReferences']['vmext:ProviderVdcReference']:
            jpvdcs[pvdc['@name']] = self.get_pvdc_details(pvdc['@href'].split('providervdc/', 1)[-1])
            
        self.pvdcs = jpvdcs
        return self.pvdcs

    def get_storage_profiles(self, pvdc):
        storage_profiles = {}
        url = 'https://%s/api/query?type=providerVdcStorageProfile&format=references&filter=providerVdc==https://%s/api/admin/providervdc/%s' % (self.vcd_host,self.vcd_host,self.pvdcs[pvdc]['ref'])
        headers = {'Accept': 'application/*+xml;version=5.1',
                   'x-vcloud-authorization': self.vcd_auth
                  }
        p = requests.get(url, headers=headers, verify=False)
        jdata = xmltodict.parse(p.text)

        for storage_profile in jdata['ProviderVdcStorageProfileReferences']['ProviderVdcStorageProfileReference']:
            storage_profiles[storage_profile['@name']] = {}
            storage_profiles[storage_profile['@name']]['id'] = storage_profile['@id']
            storage_profiles[storage_profile['@name']]['href'] = storage_profile['@href']

        return storage_profiles

    def get_network_pools(self):
        network_pools = {}
        url = 'https://%s/api/admin/extension/networkPoolReferences' % self.vcd_host
        headers = {'Accept': 'application/*+xml;version=5.1',
                   'x-vcloud-authorization': self.vcd_auth
                  }
        p = requests.get(url, headers=headers, verify=False)
        jdata = xmltodict.parse(p.text)

        for network in jdata['vmext:VMWNetworkPoolReferences']['vmext:NetworkPoolReference']:
            network_pools[network['@name']] = {}
            network_pools[network['@name']]['href'] = network['@href']
            #print network.keys()

        return network_pools

    def get_orgs(self):
        orgs = {}
        url = 'https://%s/api/org' % self.vcd_host
        headers = {'Accept': 'application/*+xml;version=5.1',
                   'x-vcloud-authorization': self.vcd_auth
                  }
        p = requests.get(url, headers=headers, verify=False)
        jdata = xmltodict.parse(p.text)
        for item in jdata['OrgList']['Org']:
            orgs[item['@name']] = {}
            orgs[item['@name']]['id'] = item['@href'].split('org/', 1)[-1]

        return orgs

    def get_org(self, org_ref=None):
        org = {}
        org['vdcs'] = {}
        url = 'https://%s/api/org/%s' % (self.vcd_host, org_ref)
        headers = {'Accept': 'application/*+xml;version=5.1',
                   'x-vcloud-authorization': self.vcd_auth
                  }
        p = requests.get(url, headers=headers, verify=False)
        jdata = xmltodict.parse(p.text)
        org['desc'] = jdata['Org']['Description'] 
        org['fullname'] = jdata['Org']['FullName'] 
        org['id'] = jdata['Org']['@id'].split('org:', 1)[-1]
        for item in jdata['Org']['Link']:
            if item['@type'] == 'application/vnd.vmware.vcloud.vdc+xml':
                org['vdcs'][item['@name']] = {}
                org['vdcs'][item['@name']]['id'] = item['@href'].split('vdc/', 1)[-1]

        return org




