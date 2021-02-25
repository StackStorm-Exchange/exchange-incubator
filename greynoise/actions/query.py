from base import GreyNoiseBaseAction
from requests.exceptions import HTTPError


class QuickIP(GreyNoiseBaseAction):
    def run(self, query):

        try:
            response = self.gn_client.query(query)
        except HTTPError as e:
            return False, e

        return True, response
