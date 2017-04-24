from st2actions.runners.pythonrunner import Action
from vdx_ssh import ssh
import logging

class createCertificate(Action):
    """
       Implements the logic to generate the nsx-controller client certficate
       This action achieves the below functionality
           1. Generates client certificate
    """

    def run(self, host=None, username=None, password=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['vip']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        auth = (str(username), str(password))
        self.logger = logging.getLogger(__name__)

        changes = {}
        changes['create_cert'] = self._create_client_certificate(host, auth)
        if not changes['create_cert']:
            self.logger.info('Nsx-controller client-certificate already present on the device: %s' % host)
            exit(1)
        else:
            self.logger.info('closing connection to %s after generating nsx-controller client-certificate successfully' %
                             host)
            return changes

    def _create_client_certificate(self, host, auth):
        '''
        Logic to generate certificate.
        '''
        self._conn = ssh.SSH(host=host, auth=auth)
        cmd = "nsx-controller client-cert generate"
        result = self._conn.read(cmd)
        result = ''.join(result)
        if 'Certificate already present' in result:
            return False
        return True

