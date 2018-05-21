from lib.xcontrolAction import XControlBaseAction


class RemoveMacToBlacklist(XControlBaseAction):
    def run(self, endsystem_ip_address=None):
        mac_address = self.xcontrol_server.get_endsystem_mac_from_ip(endsystem_ip_address)

        if mac_address is not None and mac_address != "":
            return True, {"endsystem_mac_address": mac_address}
        else:
            return False, "Could not find MAC IP"
