from lib.action import FortinetBaseAction


class CreateFirewallPolicy(FortinetBaseAction):
    def run(self, policy_id=None, payload=None):
        status = self.device.create_firewall_policy(policy_id, payload)
        if status == 200:
            return (True, status)
        return (False, status)
