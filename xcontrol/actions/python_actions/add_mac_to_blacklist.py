from lib.xcontrolAction import XControlBaseAction


class AddMacToBlacklist(XControlBaseAction):
    def run(self, endsystem_mac_address=None):
        status = self.xcontrol_server.add_mac_to_black_list(endsystem_mac_address)

        return True, status
