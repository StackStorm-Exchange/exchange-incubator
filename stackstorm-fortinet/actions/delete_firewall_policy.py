from lib.action import FortinetBaseAction

class DeleteFirewallPolicy(FortinetBaseAction):
    def run(self, policy_id=None):
        status = self.device.delete_firewall_policy(policy_id)
        if status == 200:
                return (True, status)
        return(False, status)
