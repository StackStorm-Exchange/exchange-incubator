from Tuleap.RestClient.Trackers import Tracker
from lib.base import BaseTuleapAction


class GetArtifacts(BaseTuleapAction):
    def run(self, tracker_id):
        success = self._login()
        if success:
            # Tracker
            trackers = Tracker(self.connection)
            success = trackers.request_artifact_list(tracker_id)
            if success:
                self.response = trackers.get_data()

                return True, self.response

        return False, self.response
