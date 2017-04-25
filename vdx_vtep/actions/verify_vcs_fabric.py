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

import pynos.device
from st2actions.runners.pythonrunner import Action

import logging

class VerifyVcs(Action):
    """
       Implements the logic to verify VCS Fabric
       This action achieves the below functionality
           1. Valdiates vcsId,rbridgeIDs and total nodes in VCS Fabric.
    """

    def run(self, host=None, username=None, password=None, vcs_id=None, rbridge_ids=None, nodes=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['mgmt_ip1']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        if vcs_id is None:
            vcs_id = self.config['vcs_id']

        if rbridge_ids is None:
            rbridge_ids = self.config['rbridge_id1']

        if nodes is None:
            nodes = 2

        self.logger = logging.getLogger(__name__)
        conn = (host, '22')
        auth = (username, password)

        changes = {}

        with pynos.device.Device(conn=conn, auth=auth) as device:

            changes['pre_requisites'] = self._check_requirements(device, vcs_id, rbridge_ids, nodes)
            changes['verify_vcs'] = False
            if changes['pre_requisites']:
                changes['verify_vcs'] = self._verify_vcs(device, vcs_id, rbridge_ids, nodes)
            if changes['verify_vcs']:
                self.logger.info(
                    'closing connection to %s after verifying VCS Fabric successfully!',
                    host)
                return changes
            else:
                self.logger.info(
                    'VCS Fabric Verification Failed')
                exit(1)

    def _check_requirements(self, device, vcs_id, rb_ids, nodes):
        rb_list = rb_ids.split(',')
        for id in rb_list:
            if int(id) > 239 or int(id) < 1:
                raise ValueError(' Rbridge ID: %s is Invalid. Not in <1-239> range' % id)

        if int(vcs_id) > 8192 or int(vcs_id) < 1:
            raise ValueError('VCS Id:%s is Invalid. Not in <1-8192> range' % vcs_id)

        return True


    def _verify_vcs(self, device, vcs_id, rbridge_ids, nodes):
        """VCS Fabric Varification.
        """
        try:
            output = device.vcs.vcs_nodes
        except Exception as e:
            self.logger.error(
                'VCS Fabric Verification Failed with Exception: %s' % e)
            return False

        if not output:
            return False

        if not (self._verify_vcsId(vcs_id, output)):
            self.logger.info("VCSid verification failed")
            return False
        rb_list = rbridge_ids.split(',')
        for rb_id in rb_list:
            if not (self._verify_vcsRbrideId(rb_id, output)):
                self.logger.info("Rbridge Id:%s verification failed" % rb_id)
                return False
        if not (self._verify_vcsToalNoOfNodes(nodes, output)):
            self.logger.info ("Total Number of nodes in the VCS are not equal to desired nodes %r" % (nodes))
            return False

        return True

    def _verify_vcsId(self, vcsId, output):
        result = False
        for node in output:
            if node['node-vcs-id'] == str(vcsId):
                result = True
                break
        return result

    def _verify_vcsRbrideId(self, rbridge_id, output):
        result = False

        for node in output:
            if node['node-rbridge-id'] == str(rbridge_id):
                result = True
                break
        return result


    def _verify_vcsToalNoOfNodes(self, nodes, output):
        result = False
        if len(output) == int(nodes):
            result = True
        return result

