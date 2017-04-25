# Copyright 2017 Great Software Laboratory Pvt. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from st2actions.runners.pythonrunner import Action
from vdx_ssh import ssh
import logging

class GetSwitchCertificate(Action):
    """
       Implements the logic to get the nsx-controller client certficate
       This action achieves the below functionality
           1. Reads client certificate
    """

    def run(self, host=None, username=None, password=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host=self.config['vip']

        if username is None:
            username=self.config['username']

        if password is None:
            password=self.config['password']
            
        auth = (str(username), str(password))
        self.logger = logging.getLogger(__name__)

        changes = {}
        changes['get_cert'] = self._get_client_certificate(host,auth)
        if not changes['get_cert']:
            self.logger.info('Nsx-controller client-certificate is not generated on the device: %s' % host)
            exit(1)
        else:
            self.logger.info('closing connection to %s after reading nsx-controller client-certificate successfully' %
                             host)
            return changes

    def _get_client_certificate(self,host,auth):
        '''
        Logic to read the client certificate
        Return: certificate
        '''
        self._conn = ssh.SSH(host=host, auth=auth)
        cert = self._conn.read("show nsx-controller client-cert")
        certificate = '\n'.join(cert)
        if 'BEGIN CERTIFICATE' not in certificate :
            return False
        return certificate

