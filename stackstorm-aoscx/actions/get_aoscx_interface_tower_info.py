from st2common.runners.base_action import Action
from pyaoscx import session, lldp

import json
import re
import requests


class GetAOSCXInterfaceTowerInfo(Action):
    def run(self, line, hostname, tower_ip, tower_user, tower_pass,
            proxy=None):
        """
        Called StackStorm action, parameters passed through StackStorm
        Action call
        :param line: Syslog message
        :param hostname: AOS-CX hostname found in syslog message
        :param tower_ip: Ansible Tower address to be used in REST API calls
        :param tower_user: Ansible Tower login username used in REST API calls
        :param tower_pass: Ansible Tower login password used in REST API calls
        :param proxy: Dictionary containing proxy information with keys 'http'
        and 'https'
        :return: list containing DHCP IP address found through LLDP, device
        inventory hostname, Ansible Tower inventory
        """
        global TOWER_IP, TOWER_USERNAME, TOWER_PASSWORD, PROXY_DICT

        if proxy is None:
            PROXY_DICT = {'http': None, 'https': None}
        else:
            PROXY_DICT = proxy

        TOWER_IP = tower_ip
        TOWER_USERNAME = tower_user
        TOWER_PASSWORD = tower_pass
        # retrieve interface value from syslog message
        p = re.compile(r'(\d+\/\d+\/\d+)')
        port_match = p.search(line)
        if port_match:
            port = port_match.group(1)
        else:
            self.logger.error("ERROR: Port not "
                              "found on {1} in message:\n{0}".format(line,
                                                                     hostname))
            exit(-1)
        # get newly discovered device info through LLDP informaiton
        lldp_ip_addr, mac_addr, device_current_hostname = self.get_info_link(hostname, port)  # NOQA
        # verify if that device needs to be provisioned and return it's name
        # in Ansible
        device_inventory_hostname, inventory = self.get_connected_host_tower_info(mac_addr, device_current_hostname)   # NOQA
        # returns ip_addr, device_name, inventory
        return lldp_ip_addr, device_inventory_hostname, inventory

    def get_info_link(self, hostname, port):
        """
        get the MAC address and IP address using LLDP information of the device
        connected to the specified port of an AOS-CX switch
        :param hostname: AOS-CX hostname found in syslog message
        :param port: interface who's link came up in syslog message
        :return: list of ip adress, mac address, and device name
        """
        # gets switch login info that sent syslog
        ip, username, password = self.get_syslog_host_tower_info(hostname)
        # log into AOS-CX switch
        login_url = "https://" + ip + ":443/rest/v1/"
        sesh = session.login(login_url, username, password)
        try:
            response = lldp.get_lldp_neighbor_info(int_name=port,
                                                   s=sesh, url=login_url,
                                                   depth=3)
            if not response:
                self.logger.error("Failed REST called to "
                                  "AOS-CX: {0}".format(ip))
                session.logout(s=sesh, url=login_url)
                exit(-1)
            ip_addr = None
            if response["interface"]["name"] == port:
                ip_addr_tmp = response["neighbor_info"]["mgmt_ip_list"]
                # In case both IPv4 and IPv6 addresses are found, IPv4 is used
                if ',' in str(ip_addr_tmp):
                    ip_addr_split = ip_addr_tmp.split(',')
                    for address in ip_addr_split:
                        if ':' not in address:
                            ip_addr = address
                # Protects against MAC address populating for mgmt address
                elif ':' not in str(ip_addr_tmp):
                    ip_addr = ip_addr_tmp
                else:
                    self.logger.error("\nERROR: IPv4 address not populated on"
                                      "{0} - found {1} ".format(port,
                                                                ip_addr_tmp))
                mac_addr = response["chassis_id"]
                device_name = response["neighbor_info"]["chassis_name"]
                session.logout(s=sesh, url=login_url)
                return [ip_addr, mac_addr, device_name]
        except Exception as error:
            self.logger.error("ERROR: %s", error)
            session.logout(s=sesh, url=login_url)
            exit(-1)
        # registers error if port not found on core switch
        self.logger.error("ERROR: Failed to retrieve "
                          "LLDP info port %s not found on %s", port, ip)
        session.logout(s=sesh, url=login_url)
        exit(-1)

    def get_tower_hosts(self):
        """
        executes a REST API call to retrieve all hosts in Ansible Tower
        :return: tuple of list of dicts containing all hosts in Ansible Tower,
        Ansible REST API Auth Token
        """
        global TOWER_IP, TOWER_USERNAME, TOWER_PASSWORD, PROXY_DICT
        token = self.towerLogin("https://" + TOWER_IP + "/api/v2/tokens/",
                                TOWER_USERNAME, TOWER_PASSWORD)
        auth = {'Authorization': 'Bearer ' + token}
        hosts_url = ("https://" + TOWER_IP + "/api/v2/hosts/")
        tower_response = (requests.get(hosts_url, headers=auth, verify=False,
                                       proxies=PROXY_DICT))
        self.logger.info("get_host_info status code: %s",
                         tower_response.status_code)

        if tower_response.status_code == 200:
            # Return the list of dicts of hosts and Tower Auth Token
            return json.loads(tower_response.content)["results"], auth
        else:
            self.logger.error("\nFailed to retrieve hosts from Tower:\n"
                              "Status Code: {0}\n"
                              "Tower IP: {1}\n"
                              "".format(tower_response.status_code,
                                        TOWER_IP))
            exit(-1)

    def get_syslog_host_tower_info(self, hostname):
        """
        executes a REST API call to retrieve all hosts in Ansible Tower
        inventories and searches for a device who's inventory_hostname
        matches the hostname provided
        :param hostname: str of device hostname to be matched
        :return: tuple of device's IP address, login username, and login
        password as it is stored in Ansible Tower inventory
        """
        global PROXY_DICT
        tower_hosts, tower_auth_token = self.get_tower_hosts()

        # Traverse through all hosts for matching hostname
        for elem in tower_hosts:
            if isinstance(elem, dict):
                if str(elem['name']) == str(hostname):
                    varURL = ("https://" + TOWER_IP +
                              elem["related"]["variable_data"])
                    varURLResponse = (requests.get(varURL,
                                                   headers=tower_auth_token,
                                                   verify=False,
                                                   proxies=PROXY_DICT))
                    varDict = json.loads(varURLResponse.content)
                    self.logger.info("Found host %s in Ansible inventory",
                                     hostname)
                    if all(variables in varDict.keys() for variables in ['ansible_host', 'ansible_user', 'ansible_password']):  # NOQA
                        return [varDict["ansible_host"],
                                varDict["ansible_user"],
                                varDict["ansible_password"]]
                    else:
                        self.logger.error("ERROR: Host %s has no "
                                          "ansible_host/ansible_user"
                                          "/ansible_password defined in "
                                          "Ansible inventory", hostname)
                        exit(-1)
            # registers error if host not in inventory
            else:
                self.logger.error("ERROR: Host %s not in "
                                  "Ansible inventory", hostname)
                exit(-1)
        self.logger.error("ERROR: Host %s not in Ansible inventory", hostname)

    def get_connected_host_tower_info(self, mac_address, current_hostname):
        """
        executes a REST API call to retrieve all hosts in Ansible Tower
        inventories and searches for a device who's mac_address matches the
        hostname or mac_address provided, checks if existing hostname matches
        what is defined in Ansible inventory, if it's matched then the device
        does not need to be provisioned
        :param mac_address: str of device MAC address to be matched
        :param current_hostname: str of device's current hostname found to be
        matched against inventory name
        :return: tuple of device's IP address, login username, and login
        password as it is stored in Ansible Tower inventory
        """
        tower_hosts, tower_auth_token = self.get_tower_hosts()

        # Traverse through all hosts for matching hostname
        for elem in tower_hosts:
            if isinstance(elem, dict):
                # Match if device in inventory has found MAC address in
                # inventory variables
                if mac_address in elem['variables']:
                    if str(elem['name']) == str(current_hostname):
                        self.logger.error("\n***Device already "
                                          "provisioned: {0}***"
                                          "\n".format(current_hostname))
                        exit(-1)
                    return elem['name'], elem['inventory']
            # registers error if host not in inventory
            else:
                self.logger.error("ERROR: Host %s not in "
                                  "Ansible inventory", mac_address)
        self.logger.error("ERROR: Host %s not in Ansible inventory",
                          mac_address)

    def towerLogin(self, url, username, password):
        """
        executes login REST API call to retrieve auth token to Ansible Tower
        :param url: str URL to Ansible Tower
        :param username: str login username to Ansible Tower
        :param password: str login password to Ansible Tower
        :return:
        """
        global PROXY_DICT
        login_data = (str(username), str(password))
        login_header = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, auth=login_data,
                                     headers=login_header, verify=False,
                                     timeout=5, proxies=PROXY_DICT)
            if response.status_code != 201:
                self.logger.warn('Tower Login failed...'
                                 '\nStatus Code{0} - {1}'
                                 ''.format(response.status_code,
                                           response.text))
                exit(-1)
            else:
                return response.json()['token']
        except requests.exceptions.ConnectTimeout:
            self.logger.warning('ERROR: Error connecting to '
                                'Ansible host: connection attempt timed out.')
            exit(-1)
