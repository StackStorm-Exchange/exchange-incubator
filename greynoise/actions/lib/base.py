from st2common.runners.base_action import Action
from greynoise import GreyNoise
from netaddr import *

class GreyNoiseBaseAction(Action):
    def __init__(self, config):
        super(GreyNoiseBaseAction, self).__init__(config=config)

        gn_api_key = self.config.get('gn_api_key', None)
        self.instance = GreyNoise(api_key=gn_api_key, integration_name="greynoise-stackstorm-dev")

    def validate_ip(self, ip):
        try:
            ip = IPAddress(ip)
            if ip.is_unicast() and not ip.is_private():
                return True
            else:
                return False
        except Exception as e:
            return False, e