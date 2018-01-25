from lib.action import FortinetBaseAction


class UpdateFirewallPolicy(FortinetBaseAction):
    def run(self, policy_id=None, payload=None):
        status_code = self.device.update_firewall_policy(policy_id, payload)
        if status_code == 200:
            return (True, status_code)
        return (False, status_code)
