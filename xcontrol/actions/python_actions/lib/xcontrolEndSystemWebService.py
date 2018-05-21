import requests
import urllib3
import shlex
import httplib
from xml.etree import ElementTree


class XControlEndSystemWebServiceApi(object):
    def __init__(self, xcontrol, username, password):
        self.url = 'https://{0}:8443/axis/services/NACEndSystemWebService/'.format(xcontrol)
        self.username = username
        self.password = password

    def add_mac_to_black_list(self, mac_address):
        method = 'addMACToBlacklist'
        params = {'mac': mac_address, 'description': 'StackStorm activated endpoint blacklist',
                  'reauthorize': 'true'}

        result = requests.get(url=self.url + method, auth=(self.username, self.password),
                              params=params, verify=False)

        if result.status_code != httplib.OK:
            return False
        else:
            return True

    def remove_mac_from_blacklist(self, mac_address):
        method = 'removeMACFromBlacklist'
        params = {'mac': mac_address, 'reauthorize': 'true'}

        result = requests.get(url=self.url + method, auth=(self.username, self.password),
                              params=params, verify=False)
        if result.status_code != httplib.OK:
            return False
        else:
            return True

    def get_endsystem_mac_from_ip(self, ip_address):
        method = 'getEndSystemByIP'
        params = {'ipAddress': ip_address}

        result = requests.get(url=self.url + method, auth=(self.username, self.password),
                              params=params, verify=False)

        if result.status_code != httplib.OK:
            return False, result.content

        resp_content = result.content
        tree = ElementTree.fromstring(resp_content)
        ret = tree.findall('{http://ws.web.server.tam.netsight.enterasys.com}return')
        resp_text = ret[0].text

        if 'errorCode=1' in resp_text:
            raise ValueError(resp_text)

        lexer = shlex.shlex(resp_text, posix=True)
        lexer.whitespace_split = True
        lexer.whitespace = ','
        props = dict(pair.split('=', 1) for pair in lexer)

        return props['macAddress']

    def add_mac_to_end_system_group(self, mac_address, end_system_group):
        method = 'addMACToEndSystemGroup'
        params = {'mac': mac_address, 'endSystemGroup': end_system_group,
                  'description': 'StackStorm activated endpoint blacklist',
                  'reauthorize': 'true', 'removeFromOtherGroups': 'true'}

        result = requests.get(url=self.url + method, auth=(self.username, self.password),
                              params=params, verify=False)

        if result.status_code != httplib.OK:
            return False
        else:
            return True

    def add_ip_to_end_system_group(self, ip_address, end_system_group):
        method = 'addIPToEndSystemGroup'
        params = {'ipAddress': ip_address, 'endSystemGroup': end_system_group,
                  'description': 'StackStorm activated endpoint blacklist',
                  'reauthorize': 'true', 'removeFromOtherGroups': 'true'}

        result = requests.get(url=self.url + method, auth=(self.username, self.password),
                              params=params, verify=False)

        if result.status_code != httplib.OK:
            return False
        else:
            return True


urllib3.disable_warnings()

if __name__ == "__main__":
    xcontrol = '100.252.214.185'
    username = 'admin'
    password = 'admin'
    api = XControlEndSystemWebServiceApi(xcontrol, username, password)
    result_remote = api.get_endsystem_mac_from_ip("7.7.5.10")
    print result_remote
