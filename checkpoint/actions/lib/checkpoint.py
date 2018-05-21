import json
import requests
import urllib3

class CheckpointApi(object):
    def __init__(self, checkpoint, username, password):
        self.checkpoint = checkpoint
        self.username = username
        self.password = password
        self.session = None

    def get_session_id(self):
        if self.session is None:
            data = {'user': self.username, 'password': self.password}
            content = self.post('https://{0}/web_api/login'.format(self.checkpoint), data)
            if content is not None and 'sid' in content:
                response = json.loads(content)
                self.session = response['sid']
        return self.session

    def logout(self):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {}
            status = self.post('https://{0}/web_api/logout'.format(self.checkpoint), data)
        return status

    def add_host(self, host):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {'name': host, 'ip-address': host}
            status = self.post('https://{0}/web_api/add-host'.format(self.checkpoint), data)
        return status

    def get_host(self, host):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {'name': host}
            status = self.post('https://{0}/web_api/show-host'.format(self.checkpoint), data)
        return status

    def delete_host(self, host):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {'name': host}
            status = self.post('https://{0}/web_api/delete-host'.format(self.checkpoint), data)
        return status

    def add_group(self, group, members):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {'name': group, 'members': members}
            status = self.post('https://{0}/web_api/add-group'.format(self.checkpoint), data)
        return status

    def get_group(self, group):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {'name': group}
            status = self.post('https://{0}/web_api/show-group'.format(self.checkpoint), data)
        return status

    def set_group(self, group, members):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {'name': group, 'members': members}
            status = self.post('https://{0}/web_api/set-group'.format(self.checkpoint), data)
        return status

    def delete_group(self, group):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {'name': group}
            status = self.post('https://{0}/web_api/delete-group'.format(self.checkpoint), data)
        return status

    def add_access_rule(self, name, sip, dip, position='top', action='Drop', layer='Network'):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {'name': name, 'source': sip, 'destination': dip, 'position': position, 'action': action, 'layer': layer}
            status = self.post('https://{0}/web_api/add-access-rule'.format(self.checkpoint), data)
        return status

    def get_access_rule(self, name, layer='Network'):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {'name': name, 'layer': layer}
            status = self.post('https://{0}/web_api/show-access-rule'.format(self.checkpoint), data)
        return status

    def delete_access_rule(self, name, layer='Network'):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {'name': name, 'layer': layer}
            status = self.post('https://{0}/web_api/delete-access-rule'.format(self.checkpoint), data)
        return status

    def publish(self):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            data = {}
            status = self.post('https://{0}/web_api/publish'.format(self.checkpoint), data)
        return status

    # Suspicious Activity Monitoring (SAM)
    def add_sam_rule(self, source, timeout=0, targets=None):
        status = None
        sid = self.get_session_id()
        if sid is not None:
            to = ''
            if timeout > 0:
                to = '-t {0}'.format(str(timeout))
            if targets is None:
                gateways = self.get_gateways()
                if gateways is not None:
                    targets = []
                for gateway in gateways:
                    type = gateway['type']
                    if type == 'simple-gateway':
                        targets.append(gateway['name'])
                script = 'fw sam -v -s {0} -f all {1} -J src {2}'.format(self.checkpoint, to, source)
                data = {'script-name': 'add-sam-rule', 'script': script, 'targets': targets}
                status = self.post('https://{0}/web_api/run-script'.format(self.checkpoint), data)
        return status

    def get_gateways(self):
        gateways = None
        sid = self.get_session_id()
        if sid is not None:
            data = {}
            content = self.post('https://{0}/web_api/show-gateways-and-servers'.format(self.checkpoint), data)
            if content is not None and 'objects' in content:
                response = json.loads(content)
                gateways = response['objects']
        return gateways

    def post(self, url, data):
        content = None
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        if self.session is not None:
            headers['X-chkp-sid'] = self.session
        r = requests.post(url, verify=False, headers=headers, json=data)
        code = r.status_code
        if code == 200:
            content = r.content
        elif code != 404:
            print '{0} -> {1}'.format(str(code), r.content)
        return content

    def add_threat(self, threat, group='Block IPs'):
        status =  None
        publish = False
        sid = self.get_session_id()
        if sid is not None:
            address = self.get_host(threat)
            if address is None:
                print 'Adding host object: {0}'.format(threat)
                self.add_host(threat)
                publish = True
            block = self.get_group(group)
            if block is None:
                print 'Adding address group: {0}'.format(group)
                status = self.add_group(group, threat)
                publish = True
            else:
                response = json.loads(block)
                list = []
                members = response['members']
                for member in members:
                    name = member['name']
                    list.append(name)
                if threat not in list:
                    list.append(threat)
                    print 'Updating address group: {0} with members: {1}'.format(group, list)
                    status = self.set_group(group, list)
                    publish = True
                else:
                    status = "{\"message\": \"threat: " + threat + " is already in group\"}"
            dip = self.get_access_rule('DENY DIP')
            if dip is None:
                print 'Adding deny DIP rule'
                self.add_access_rule('DENY DIP', 'Any', 'Block IPs')
                publish = True
            sip = self.get_access_rule('DENY SIP')
            if sip is None:
                print 'Adding deny SIP rule'
                self.add_access_rule('DENY SIP', 'Block IPs', 'Any')
                publish = True
            if publish:
                self.publish()
        else:
            status = "{\"message\": \"Could not get checkpoint session id\"}"

        response = self.logout()
        return status

    def remove_threat(self, threat, group='Block IPs'):
        status = None
        publish = False
        sid = self.get_session_id()
        if sid is not None:
            block = self.get_group(group)
            if block is not None:
                response = json.loads(block)
                list = []
                members = response['members']
                for member in members:
                    name = member['name']
                    if name == threat:
                        publish = True
                    else:
                        list.append(name)
                if publish:
                    print 'Updating address group: {0} with members: {1}'.format(group, list)
                    status = self.set_group(group, list)
            delete = self.delete_host(threat)
            if delete is not None:
                print 'Deleted host object: {0}'.format(threat)
                publish = True
            else:
                status = "{\"message\": \"threat: " + threat + " is not in group\"}"
            if publish:
                self.publish()
        else:
           status = "{\"message\": \"Could not get checkpoint session id\"}"

        response = self.logout()
        return status

urllib3.disable_warnings()

if __name__ == "__main__":
    checkpoint = '10.52.23.34'
    username = 'admin'
    password = 'admin'
    threat = '192.168.10.32'
    api = CheckpointApi(checkpoint, username, password)
    response = api.add_threat(threat)
    print response

    #response = api.remove_threat(threat)
    #print response
