from st2actions.runners.pythonrunner import Action
import re

class PublishConfigs(Action):
    def __init__(self, config=None):
        super(PublishConfigs, self).__init__(config=config)
        
    def run(self):
        configs = {}
        
        configs['vip'] = self.config['vip']
        configs['username'] = self.config['username']
        configs['password'] = self.config['password']
        configs['overlay_gateway_name'] = self.config['overlay_gateway_name']
        
        
                
        return configs
        
    