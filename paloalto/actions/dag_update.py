import sys
import requests
import xmltodict
import json
import urllib3
from string import Template
from st2actions.runners.pythonrunner import Action

class UpdateDAG(Action):
       
    def run(self, ip, firewall):
        _result = {}
        _uid_message = """
        <uid-message>
        <version>2.0</version>
        <type>update</type>
        <payload>
        <register>
        <entry ip=${ip}>
        <tag>
        <member>${tag}</member>
        </tag>
        </entry>
        </register>
        </payload>
        </uid-message>
        """
        _tag = self.config['tag']
        _key = self.config['api_key']
        # print(_key, self.config['fws_ips'], _tag)                
        xml = Template(_uid_message)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # for firewall in self.config['fws_ips'].split(","):
        # print(ip, firewall)                
        url='https://{}/api'.format(firewall)
        try:
            response = requests.post(url + "/?type=user-id&cmd={}&key={}".
                format(xml.substitute(ip='"{}"'.format(ip), tag=_tag), _key),verify=False, timeout=5)
            # print("{}\nfirewall {} ip {} tag {}".format(response.text, firewall, ip , _tag))                                 
        except requests.exceptions.ConnectionError:
            # print("Post {}: ConnectionError".format(firewall))
            _result['"{}"'.format(firewall)] = "ConnectionError"
            return (False, _result)
        doc = json.loads(json.dumps(xmltodict.parse(response.text)))                
        if 'success' in doc['response']['@status']:
            _result[firewall] = 'success'
        else:
            _result['"{}"'.format(firewall)] = "{} : {} {}".format(doc['response']['@status'], 
                doc['response']['msg']['line']['uid-response']['payload']['register']['entry']['@ip'],
                doc['response']['msg']['line']['uid-response']['payload']['register']['entry']['@message'])                       
            # print(doc['response'])
        # print("result {}".format(_result))   
        return (True, _result)             

    