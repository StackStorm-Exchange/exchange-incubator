from st2common.runners.base_action import Action

from xcontrolEndSystemWebService import XControlEndSystemWebServiceApi


class XControlBaseAction(Action):
    def __init__(self, config):
        super(XControlBaseAction, self).__init__(config)
        self._xcontrol_ip = self.config['xcontrol_ip']
        self._username = self.config['username']
        self._password = self.config['password']
        self.xcontrol_server = self.xcontrol_server()

    def xcontrol_server(self):
        xcontrol_server = XControlEndSystemWebServiceApi(xcontrol=self._xcontrol_ip, username=self._username,
                                               password=self._password)

        return xcontrol_server
