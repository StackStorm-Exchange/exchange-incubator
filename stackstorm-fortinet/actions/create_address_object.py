from lib.action import FortinetBaseAction

class CreateAddressObject(FortinetBaseAction):
    def run(self, name=None, payload=None):
        status = self.device.create_firewall_address(name, payload)
        if status == 200:
            return (True, status)
        return (False, status)
