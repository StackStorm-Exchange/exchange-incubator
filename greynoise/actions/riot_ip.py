from base import GreyNoiseBaseAction
from requests.exceptions import HTTPError


class RiotIP(GreyNoiseBaseAction):
    def run(self, ip):
        if self.validate_ip(ip):
            try:
                response = self.gn_client.riot(ip)
            except HTTPError as e:
                return False, e

            return True, response
        else:
            return False, "Invalid IP Provided"
