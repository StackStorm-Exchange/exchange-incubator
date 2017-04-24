from vdx_ssh import ssh
import logging
import time
import socket
from st2actions.runners.pythonrunner import Action
class ConfigureVcs(Action):
    """
       Implements the logic to recreate VCS Fabric.(scenario in which VCS already formed.)
       This action achieves the below functionality
           1. VcsId and rbridgeID Validation.
           2. VCS fabric configuration.
           3. Validates if device reboots after VCS configuration.
    """

    def run(self, host=None, username=None, password=None, vcs_id=None, rbridge_id=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            self._host = self.config['vip']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        if vcs_id is None:
            vcs_id = self.config['vcs_id']

        if rbridge_id is None:
            rbridge_id = self.config['rbridge_id1']


        auth = (str(username), str(password))
        changes = {}


        self.logger = logging.getLogger(__name__)


        changes['pre_requisites'] = self._check_requirements(vcs_id,rbridge_id)
        changes['create_vcs'] = False
        if changes['pre_requisites']:
            changes['create_vcs'] = self._configure_vcs(vcs_id, rbridge_id, host, auth)
        else:
            self.logger.info('Pre-requisites validation failed for interface configuration')
        if not changes['create_vcs']:
            self.logger.info(
                    'VCS Fabric configuration Failed on the device %s' % host)
            exit(1)
        else:
            self.logger.info('closing connection to %s after successful VCS Fabric configuring' %
                    host)
            return changes

    def _check_requirements(self,vcs_id,rbridge_id):
        """
        Verify if VCS Fabric pre-exists with multiple nodes.
        """
        if int(vcs_id) > 8192 or int(vcs_id) < 1:
            raise ValueError('VCS Id is Invalid. Not in <1-8192> range')
        if int(rbridge_id) > 239 or int(rbridge_id) < 1:
            raise ValueError(' Rbridge ID is Invalid. Not in <1-239> range')

        return True


    def _configure_vcs(self, vcs_id, rb_id, host,auth):
        """Configuring VCS Fabric
        """

        self._conn = ssh.SSH(host=host, auth=auth)
        self.logger.info ("Creating VCS Fabric on the device: %r with vcsId:%r and rbridgeId: %r" % (host, vcs_id, rb_id))
        cmd = "vcs vcsid %s set-rbridge-id %s" % (vcs_id, rb_id)
        try:
            self._conn.send(cmd)
            self._conn.send("y")
        except Exception as e:
            self.logger.error('Command: %s execution failed with Exception %s' %(cmd, e))
        result = self._if_device_reboot(host)
        if not result:
            self.logger.info('Device:%s is not rebooted after VCS configuration' %host)
        return result

    def _if_device_reboot(self,host):

        # Logic to check if device has rebooted.

        self.logger.info ("Checking if the device is rebooted after VCS command execution")
        result = 0
        t_elapsed = 1
        while t_elapsed < 120:
            response = self._verify_ssh_connectivity(ip=host)
            if response == 0:
                t_elapsed += 10
                time.sleep(10)
            else:
                result = 1
                time.sleep(10)
                self.logger.info('Device is rebooted after VCS configuration.')
                break
        return result

    def _verify_ssh_connectivity(self,**kwargs):
        ip = kwargs.pop('ip')
        port = kwargs.pop('port', 22)
        response = None
        try:
            socket.setdefaulttimeout(5)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            response = s.connect_ex((ip, port))
            s.close()
            return response
        except:
            return response


