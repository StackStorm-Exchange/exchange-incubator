import time
import logging
import pynos.device
from st2actions.runners.pythonrunner import Action


class VerifyVcsReady(Action):
    """
       Implements the logic to wait untill VCS Fabric is up
       This action achieves the below functionality
           1. Validates if vcs Fabric is ready to use
    """

    def run(self, host, username, password,nodes):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['mgmt_ip1']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']
        if nodes is None:
            nodes = 2
        self.logger = logging.getLogger(__name__)
        conn = (host, '22')
        auth = (username, password)

        changes = {}

        changes['verify_vcs_ready'] =  False
        changes['verify_vcs_ready'] = self._verify_vcs_ready( nodes, conn, auth)
        if changes['verify_vcs_ready']:
            self.logger.info(
                'closing connection to %s after verifying if VCS Formation is complete.',
                    host)
            return changes
        else:
            self.logger.info(
                'Total Nodes in VCS are not equal to the expected nodes: %s' %nodes)
            self.logger.info('VCS Fabric is not ready with expected nodes.')
            exit(1)


    def _verify_vcs_ready(self,  nodes, conn, auth):
        """Waits till VCS Fabric formation is completed.
        """
        # Logic to check if VCS Fabric formation is ready and its online
        # Wait for max:10 min as VCS formation can take upto 10 min after device reboots
        ready = False
        for t in range(30):
            try:
                device = pynos.device.Device(conn=conn, auth=auth)
                output = device.vcs.vcs_nodes

                if len(output) == int(nodes):
                    self.logger.info('VCS Fabric is ready')
                    ready = True
                    break
                if not ready:
                    self.logger.info('VCS Formation is in progress')
                    self.logger.info('Trying Again after 30 sec')
                    time.sleep(30)

            except Exception as e:
                self.logger.info('%s' % e)
                self.logger.info('Trying Again after 30 sec')
                time.sleep(30)
        return ready





