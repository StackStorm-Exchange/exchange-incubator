
from lib.xcontrolAction import XControlBaseAction


class RemoveMacFromBlacklist(XControlBaseAction):
    def run(self, endsystem_mac_address=None):
        status = self.xcontrol_server.remove_mac_from_blacklist(endsystem_mac_address)

        return True, status
