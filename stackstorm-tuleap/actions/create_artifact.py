from Tuleap.RestClient.Artifacts import Artifacts
from lib.base import BaseTuleapAction


class CreateArtifact(BaseTuleapAction):
    def run(self, tracker_id, values_by_field):
        success = self._login()
        if success:
            # Artifacts
            artifacts = Artifacts(self.connection)
            success = artifacts.create_artifact(tracker_id, values_by_field)
            if success:
                self.response = artifacts.get_data()

                return True, self.response

        return False, self.response
