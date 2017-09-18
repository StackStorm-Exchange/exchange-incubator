import sys
from lib.jsonrpc import JsonRPC
from st2actions.runners.pythonrunner import Action

class ExosCmd(Action):

    def run(self, ipaddress='10.68.65.81', cmd=''):
        """
        Run an EXOS command on the remote switch

        Args:
            - ip_address: The IP address of the switch
            - username: login user name
            - password: login password
            - cmd: either a single EXOS command or list of EXOS commands

        Raises:
            - ValueError: On switch reponse being invalid
            - RuntimeError: if switch cannot process the command


        Returns:
            dict: with EXOS CLI results
        """

        jsonrpc = JsonRPC(ipaddress, self.config['username'], self.config['password'])
        jsonrpc.cookie = self.action_service.get_value('cookie')

        try:
            response = jsonrpc.send(cmd)
            self.action_service.set_value(name='cookie', value=jsonrpc.cookie)
            return response
        except Exception:
            sys.exit(1)
