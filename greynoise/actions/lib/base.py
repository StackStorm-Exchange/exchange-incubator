import re
from netaddr import IPAddress
from st2common.runners.base_action import Action
from os import path

from greynoise import GreyNoise

BASEPATH = path.dirname(__file__)
FILEPATH = path.abspath(path.join(BASEPATH, "..", "..", "pack.yaml"))

ENRICH_STRING = open(FILEPATH, 'r').read()
PACK_VERSION = re.search(r'version:\s(.*)', ENRICH_STRING).group(1)


class GreyNoiseBaseAction(Action):
    def __init__(self, config):
        super(GreyNoiseBaseAction, self).__init__(config=config)

        gn_api_key = self.config.get('greynoise_api_key', None)
        self.gn_client = GreyNoise(
            api_key=gn_api_key,
            integration_name="greynoise-stackstorm-v" + PACK_VERSION
        )

    def validate_ip(self, ip):
        ip = IPAddress(ip)
        if ip.is_unicast() and not ip.is_private():
            return True
        else:
            return False
