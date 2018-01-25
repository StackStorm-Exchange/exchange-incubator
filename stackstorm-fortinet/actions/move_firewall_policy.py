from lib.action import FortinetBaseAction


class MoveFirewallPolicy(FortinetBaseAction):
    def run(self, policy_id=None, position=None, neighbor=None):
        status = self.device.move_firewall_policy(policy_id, position, neighbor)
        if status == 200:
            return (True, status)
        return (False, status)
