import json

from lib.action import CheckpointBaseAction


class CreateAddressGroup(CheckpointBaseAction):
    def run(self, threat_ip=None):
        status = self.device.add_threat(threat_ip)

        if status is not None:
            result = json.loads(status)
            if 'meta-info' in result:
                if result['meta-info']['validation-state'] == 'ok':
                    return True, 0
        return False, status
