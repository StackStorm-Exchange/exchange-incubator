from NSX.nsx import NSX
from st2actions.runners.pythonrunner import Action

class AddHardwareVtep(Action):
    def __init__(self, config=None, action_service=None):
        super(AddHardwareVtep, self).__init__(config=config, action_service=action_service)
        
    def run(self):
        configs = {}
        
        configs['lswitch_name'] = self.config['lswitch_name']
        configs['nsx_mgr_ip'] = self.config['nsx_mgr_ip']
        configs['nsx_mgr_pass'] = self.config['nsx_mgr_pass']
        configs['nsx_mgr_user'] = self.config['nsx_mgr_user']
        configs['port_name'] = self.config['port_name']
        configs['switch_name'] = self.config['switch_name']
        configs['vlan'] = self.config['vlan']
        configs['vtep_name'] = self.config['vtep_name']
        
        return configs
        
        
