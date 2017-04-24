from st2actions.runners.pythonrunner import Action
import pynos.device

class CreateVe(Action):
    def __init__(self, config=None):
        super(CreateVe, self).__init__(config=config)
        
    def run(self, host=None, username=None, password=None, rbridge_id=None, ve_vlan=None, ve_ip=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['vip']
            
        if username is None:
            username = self.config['username']
            
        if password is None:
            password = self.config['password']
            
        if rbridge_id is None:
            rbridge_id = self.config['rbridge_id1']
        
        if ve_vlan is None:
            ve_vlan = self.config['ve_vlan']
            
        if ve_ip is None:
            ve_ip = self.config['ve_ip']
        
        conn = (host, '22')
        auth = (username, password)
        changes = {}
        
        with pynos.device.Device(conn=conn, auth=auth) as device:
            changes['create_ve'] = self._create_ve(device, rbridge_id=rbridge_id, ve_name=ve_vlan, ip_address=ve_ip)
            changes['set_active'] = self._set_ve_active(device, ve_name=ve_vlan, rbridge_id=rbridge_id)
        return changes

    def _create_ve(self, device, rbridge_id, ve_name, ip_address):
        """ Configuring the VE"""

        try:
            self.logger.info('Creating VE %s on rbridge-id %s', ve_name, rbridge_id)
            device.interface.add_vlan_int(ve_name)
            output = device.interface.ip_address(int_type='ve', name=ve_name, ip_addr=ip_address, rbridge_id=rbridge_id)
            #device.interface.create_ve(enable=True, ve_name=ve_name, rbridge_id=rbridge_id)
        except (ValueError, KeyError):
            self.logger.info('Invalid Input values while creating to Ve')
            
        return output
        
    def _set_ve_active(self, device, ve_name, rbridge_id):
        output = device.interface.admin_state(int_type='ve', name=ve_name, enabled=True, rbridge_id=rbridge_id)
        return output