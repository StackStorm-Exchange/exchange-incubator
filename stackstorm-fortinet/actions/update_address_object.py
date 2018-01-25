from lib.action import FortinetBaseAction

class UpdateAddressObject(FortinetBaseAction):
    def run(self, name=None, payload=None):
        status_code = self.device.update_firewall_address(name, payload)
        if status_code == 200:
            return (True, status_code)
        return (False, status_code)
