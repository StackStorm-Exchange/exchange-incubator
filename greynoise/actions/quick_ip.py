from base import GreyNoiseBaseAction
from requests.exceptions import HTTPError


class QuickIP(GreyNoiseBaseAction):
    def run(self, ip):

        try:
            response = self.gn_client.quick(ip)
        except HTTPError as e:
            return False, e

        return True, response
