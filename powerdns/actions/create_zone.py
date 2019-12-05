from lib.base import PowerDNSClient
from st2actions.runners.pythonrunner import Action

class CreateZone(Action):
    """
    Create a new zone.
    """
    def run(self, name):
        client = PowerDNSClient()
        client.create_zone(name)
