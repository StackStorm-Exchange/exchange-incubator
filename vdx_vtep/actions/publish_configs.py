from st2actions.runners.pythonrunner import Action
import re

class PublishConfigs(Action):
    def __init__(self, config=None):
        super(PublishConfigs, self).__init__(config=config)
        
    def run(self):
        configs = {}
        
        configs['vip'] = self.config['vip']
        configs['mgmt_ip1'] = self.config['mgmt_ip1']
        configs['mgmt_ip2'] = self.config['mgmt_ip2']
        configs['vcs_id'] = self.config['vcs_id']
        configs['username'] = self.config['username']
        configs['password'] = self.config['password']
        configs['rbridge_id1'] = self.config['rbridge_id1']
        configs['rbridge_id2'] = self.config['rbridge_id2']
        configs['ve_ip'] = self.config['ve_ip']
        configs['ve_vlan'] = self.config['ve_vlan']
        configs['vlan'] = self.config['vlan']
        configs['intf_name'] = self.config['intf_name']
        configs['intf_ip'] = self.config['intf_ip']
        configs['intf_type'] = self.config['intf_type']
        configs['overlay_gateway_name'] = self.config['overlay_gateway_name']
        configs['intf_name1'] = self.config['intf_name1']
        configs['intf_name2'] = self.config['intf_name2']
        configs['nsx_cnt_ip'] = self.config['nsx_cnt_ip']
        configs['nsx_cnt_name'] = self.config['nsx_cnt_name']
        configs['nsx_cnt_port'] = self.config['nsx_cnt_port']
        configs['vcenter_name'] = self.config['vcenter_name']
        configs['vcenter_pass'] = self.config['vcenter_pass']
        configs['vcenter_url'] = self.config['vcenter_url']
        configs['vcenter_user'] = self.config['vcenter_user']
        configs['vip_mask'] = self.config['vip_mask']
        configs['rbridge_ids'] = self.config['rbridge_id1'] + "," + self.config['rbridge_id1']
        configs['switch_ports'] = self._get_switch_ports()
                
        return configs
        
    def _get_switch_ports(self):
        switch_port_re = r"^intf_name[0-9]"
        switch_ports = ""
        for k in self.config:
            if re.search(switch_port_re, k):
                switch_ports += self.config[k] + ","
        return switch_ports