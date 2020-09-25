from st2common.runners.base_action import Action
from pyaoscx import session, interface, common_ops

import json


class GetLinkStatus(Action):
    def run(self, ip, username, password, proxy=None):
        """
        Gets the link status of all interfaces on an AOS-CX switch
        :param ip:  Address to be used in REST API calls
        :param username: Switch login username used in REST API calls
        :param password: Switch login password used in REST API calls
        :param proxy: Dictionary containing proxy information with keys 'http'
        and 'https'
        :return: str of all interfaces link statuses present on the switch
        """
        if proxy is None:
            proxy = {'http': None, 'https': None}

        return self._reformat_dict(self.get_link_status(ip, username, password,
                                                        proxy))

    def _reformat_dict(self, d):
        """
        formats the dict result of interface link statuses
        to str value
        :param d: dict REST API result of interface statuses
        :return: str of REST API result of interface statuses
        """
        result = ""
        for key in d:
            result = result + key + ": " + d[key] + "\n"
        return result

    def get_link_status(self, ip, username, password, proxy):
        """
        executes REST API call to AOS-CX switch and retrieves the given
        switch's interfaces and their link status
        :param ip:  Address to be used in REST API calls
        :param username: Switch login username used in REST API call
        :param password: Switch login password used in REST API call
        :param proxy: Dictionary containing proxy information with keys 'http'
        and 'https'
        :return: dict of all interfaces link statuses present on the switch
        """
        # log into AOS-CX switch
        login_url = "https://" + ip + ":443/rest/v1/"

        sesh = session.login(login_url, username, password)
        response = interface.get_all_interfaces(s=sesh, url=login_url)
        if not response:
            self.logger.error("Failed REST called to "
                              "AOS-CX: {0}".format(ip))
            session.logout(s=sesh, url=login_url)
            exit(-1)
        try:
            # create a dictionary of each interface's link status
            link_stat_dict = {}
            for int_url in response:
                # Takes string after last '/'
                port_num = int_url[(int_url.rfind('/') + 1):]
                # Ignore bridge_normal interface
                if port_num == "bridge_normal":
                    continue
                int_response = (sesh.get("https://" + ip + int_url,
                                         verify=False,
                                         proxies=proxy))
                link_state = json.loads(int_response.text)["link_state"]
                port_num = common_ops._replace_percents(port_num)
                link_stat_dict[port_num] = link_state
            # logs out of the core switch
            session.logout(s=sesh, url=login_url)
            return link_stat_dict
        except Exception as error:
            self.logger.error("ERROR: %s", error)
            session.logout(s=sesh, url=login_url)
            exit(-1)
