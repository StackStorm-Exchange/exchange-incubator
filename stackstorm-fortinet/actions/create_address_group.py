from lib.action import FortinetBaseAction


class CreateAddressGroup(FortinetBaseAction):
    def run(self, name=None, payload=None):
        status = self.device.create_address_group(name, payload)
        if status == 200:
            return (True, status)
        return (False, status)
