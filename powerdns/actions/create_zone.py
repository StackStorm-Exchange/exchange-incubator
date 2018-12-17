from lib.base import PowerDNSClient


class CreateZone(Action):
    """
    Create a new zone.
    """
    def run(self, appointment):
        client = PowerDNSClient()
        client.create_zone()
