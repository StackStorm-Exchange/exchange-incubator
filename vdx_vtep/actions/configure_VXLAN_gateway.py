import pynos.device
import pynos.utilities
from st2actions.runners.pythonrunner import Action

class ConfigureVxlanGateway(Action):
    """
       Implements the logic to set VXLAN Overlay Gateway in VCS fabric.
       This action acheives the below functionality
        1. Create VXLAN Gateway
        2. Attach rbridgeId,loopback interface
        3. Activate VXLAN Gateway
    """

    def __init__(self, config=None):
        super(ConfigureVxlanGateway, self).__init__(config=config)

    def run(self, host=None, username=None, password=None, overlay_gateway_name=None, rbridge_ids=None,
            intf_name=None, vlan=None):
        """Run helper methods to implement the desired state.
        """
        
        if host is None:
            host = self.config['vip']

        if username is None:
            username = self.config['username']

        if password is None:
            password = self.config['password']

        if overlay_gateway_name is None:
            overlay_gateway_name = self.config['overlay_gateway_name']

        if rbridge_ids is None:
            rbridge_id1 = self.config['rbridge_id1']


        if intf_name is None:
            intf_name = self.config['intf_name']

        if vlan is None:
            vlan = self.config['vlan']
            
        conn = (host, '22')
        auth = (username, password)

        #self.setup_connection(host=host, user=username, passwd=password)
        changes = {}

        with pynos.device.Device(conn=conn, auth=auth) as dev:
            changes['pre_requisites'] = self._check_requirements(dev, intf_name, vlan)
            changes['configure_overlaygw'] = False
            if changes['pre_requisites']:
                changes['configure_overlaygw'] = self._configure_overlay_gw(dev, overlay_gateway_name, rbridge_ids,
                                                                     intf_name)
            else:

                self.logger.info(
                    'Pre-requisites validation failed for overlay-gateway configuration')

            if not changes['configure_overlaygw']:
                self.logger.info(
                    'overlay-gateway configuration Failed')
                exit(1)
            else:
                self.logger.info(
                    'closing connection to %s after configuring overlay-gateway successfully!',
                    host)
                return changes

    def _configure_overlay_gw(self, dev, overlay_gateway_name, rbridge_ids,intf_name):

        result = self._set_overlaygw_name(dev, overlay_gateway_name)
        if result:
            result = self._add_rbridgeid(dev, overlay_gateway_name, rbridge_ids)

        if result:
            result = self._add_loopback_interface(dev, overlay_gateway_name, intf_name)
        if result:
            result = self._activate_hwvtep(dev, overlay_gateway_name)
        return result

    def _check_requirements(self, dev, intf_name, vlan):
        """ Verify if the Hardware already exists
        """
        if not pynos.utilities.valid_vlan_id(vlan):
            raise ValueError("VlandId %s must be between `1` and `8191`" % vlan)

        if int(intf_name) not in range(256):
            raise ValueError('Invlaid Loopback Interface Id: %s' % intf_name)

        output = dev.interface.ve_interfaces
        # Logic to check if loopback interface is precreated and active
        is_loopback_interface_present = False
        for each_int in output:
            if each_int['interface-type'] == 'loopback' and each_int['interface-name'] == str(intf_name):
                is_loopback_interface_present = True
                if each_int['interface-state'] == 'down':
                    raise ValueError("Loopback interface:%s state is down" % intf_name)

        if not is_loopback_interface_present:
            raise ValueError("Interface Loopback:%s doesn't exist" % intf_name)

        # Logic to check if vlan is precreated
        is_vlan_exist = False
        output = dev.interface.vlans
        for each_vlan in output:
            if 'vlan-id' in each_vlan and each_vlan['vlan-id'] == str(vlan):
                is_vlan_exist = True
        if not (is_vlan_exist):
            raise ValueError("VlanId %s does not exists" % vlan)

        # logic to check if overlay-Gateway is already present
        if (dev.hw_vtep.get_overlay_gateway()):
            self.logger.info('Overlay-Gateway already configured on the dev')
            return False
        return True

    def _set_overlaygw_name(self, dev, overlay_gateway_name):
        try:
            dev.hw_vtep.hwvtep_set_overlaygw_name(name=overlay_gateway_name)
            return True

        except Exception as e:
            self.logger.error(
                'Configuring Overlay-Gateway %s Failed with Exception: %s' % (e, overlay_gateway_name))
            return False

    def _add_rbridgeid(self, dev, overlay_gateway_name, rb_range):
        try:
            dev.hw_vtep.hwvtep_add_rbridgeid(name=overlay_gateway_name, rb_range=rb_range)
            return True

        except Exception as e:
            self.logger.error(
                'Configuring Overlay-Gateway %s Failed with Exception: %s' % (e, overlay_gateway_name))
            return False

    def _add_loopback_interface(self, dev, overlay_gateway_name, intf_name):
        try:
            dev.hw_vtep.hwvtep_add_loopback_interface(name=overlay_gateway_name, int_id=intf_name)
            return True
        except Exception as e:
            self.logger.error(
                'Configuring Overlay-Gateway %s Failed with Exception: %s' % (e, overlay_gateway_name))
            return False

    def _attach_vlan_vid(self, dev, overlay_gateway_name, vlan):
        try:
            dev.hw_vtep.hwvtep_attach_vlan_vid(name=overlay_gateway_name, vlan=vlan)
            return True
        except Exception as e:
            self.logger.error(
                'Configuring Overlay-Gateway %s Failed with Exception: %s' % (e, overlay_gateway_name))
            return False

    def _activate_hwvtep(self, dev, overlay_gateway_name):
        try:
            dev.hw_vtep.hwvtep_activate_hwvtep(name=overlay_gateway_name)
            return True
        except Exception as e:
            self.logger.error(
                'Configuring Overlay-Gateway %s Failed with Exception: %s' % (e, overlay_gateway_name))
            return False
