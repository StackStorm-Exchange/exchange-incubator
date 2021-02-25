from netaddr import IPAddress
from st2common.runners.base_action import Action

from greynoise import GreyNoise

PACK_VERSION = "v1.0.0"


class GreyNoiseBaseAction(Action):
    def __init__(self, config):
        super(GreyNoiseBaseAction, self).__init__(config=config)

        gn_api_key = self.config.get('greynoise_api_key', None)
        self.gn_client = GreyNoise(
            api_key=gn_api_key,
            integration_name="greynoise-stackstorm-" + PACK_VERSION
        )

    def validate_ip(self, ip):
        ip = IPAddress(ip)
        if ip.is_unicast() and not ip.is_private():
            return True
        else:
            return False
