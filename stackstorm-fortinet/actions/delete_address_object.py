from lib.action import FortinetBaseAction

class DeleteAddressObject(FortinetBaseAction):
    def run(self, name=None):
        status = self.device.delete_firewall_address(name)
        if status == 200:
                return (True, status)
        return(False, status)
