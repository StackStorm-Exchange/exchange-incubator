from lib.action import FortinetBaseAction


class UpdateAddressGroup(FortinetBaseAction):
    def run(self, name=None, payload=None):
        status_code = self.device.update_address_group(name, payload)
        if status_code == 200:
            return (True, status_code)
        return (False, status_code)
