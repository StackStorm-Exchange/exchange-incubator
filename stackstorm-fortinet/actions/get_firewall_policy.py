from lib.action import FortinetBaseAction

class GetFirewallPolicy(FortinetBaseAction):
    def run(self, name_or_id=None):
        addresses = self.device.get_firewall_policy(name_or_id)
        if isinstance(addresses, list):
                return (True, addresses)
        return(False, addresses)
