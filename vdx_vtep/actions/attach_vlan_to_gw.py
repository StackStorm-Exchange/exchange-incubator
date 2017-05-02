from vdx_ssh import ssh
import pynos.device
import pynos.utilities
import logging
from st2actions.runners.pythonrunner import Action

class attachVlanToGw(Action):
    def run(self, host=None, username=None, password=None, overlay_gateway_name=None, vlan=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            self._host = self.config['vip']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        if overlay_gateway_name is None:
            overlay_gateway_name = self.config['overlay_gateway_name']

        self.logger = logging.getLogger(__name__)

        if vlan is None:
            vlan = self.config['vlan']

        conn = (host, '22')
        auth = (str(username), str(password))
        changes = {}

        self.logger = logging.getLogger(__name__)
        dev = pynos.device.Device(conn=conn, auth=auth)

        changes['pre_requisites'] = self._check_requirements(dev, overlay_gateway_name, vlan)
        changes['attach_vlan'] = False
        if changes['pre_requisites']:
            changes['attach_vlan'] = self._attach_vlan(host, username, password, overlay_gateway_name, vlan)
        else:
            self.logger.info('Pre-requisites validation failed while attaching VLAN to overlay gateway')
        if not changes['attach_vlan']:
            self.logger.info('Attach VLAN to overlay gateway has failed.')
            exit(1)
        else:
            self.logger.info('closing connection to %s after attaching VLAN to overlay gateway' % host)
            return changes

    def _check_requirements(self, dev, overlay_gateway_name, vlan):
        if not pynos.utilities.valid_vlan_id(vlan):
            raise ValueError("VlandId %s must be between `1` and `8191`" % vlan)

        # Logic to check if vlan is precreated
        is_vlan_exist = False
        output = dev.interface.vlans
        for each_vlan in output:
            if 'vlan-id' in each_vlan and each_vlan['vlan-id'] == str(vlan):
                is_vlan_exist = True
        if not (is_vlan_exist):
            raise ValueError("VlanId %s does not exists" % vlan)

        # logic to check if overlay-Gateway is already present and vlan is already attached.
        result = dev.hw_vtep.get_overlay_gateway()
        if (not result):
            self.logger.info(' No Overlay-Gateway configured on the device')
            return False
        else:
            if result['name'] == str(overlay_gateway_name):
                if 'attached-vlan' in result:
                    if (str(vlan) in result['attached-vlan']):
                        self.logger.info('VLAN: %s is already attached to overlay gateway.' % vlan)
                        return False
            else:
                self.logger.info('Overlay gateway: %s not configured on the switch.' % overlay_gateway_name)
                return False
        return True


    def _attach_vlan(self, host, username, password, overlay_gateway_name, vlan):
        self._conn = ssh.SSH(host=host, auth=(username, password))

        try:
            cmd = "configure"
            self._conn.send(cmd)
            cmd = "overlay-gateway %s" % (overlay_gateway_name)
            self._conn.send(cmd)
            cmd = "attach vlan %d" % (int(vlan))
            self._conn.send(cmd)
        except Exception as e:
            self.logger.error('Command: %s execution failed with Exception %s' %(cmd, e))

        return True
