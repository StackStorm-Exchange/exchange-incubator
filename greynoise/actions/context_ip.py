from base import GreyNoiseBaseAction
from requests.exceptions import HTTPError


class ContextIP(GreyNoiseBaseAction):
    def run(self, ip):

        try:
            response = self.gn_client.ip(ip)
        except HTTPError as e:
            return False, e

        return True, response
