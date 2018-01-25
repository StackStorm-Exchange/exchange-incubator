from lib.action import FortinetBaseAction


class DeleteAddressGroup(FortinetBaseAction):
    def run(self, name=None):
        status = self.device.delete_address_group(name)
        if status == 200:
                return (True, status)
        return(False, status)
