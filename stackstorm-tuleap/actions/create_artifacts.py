from Tuleap.RestClient.Artifacts import Artifacts
from lib.base import BaseTuleapAction


class CreateArtifacts(BaseTuleapAction):
    def run(self, tracker_id, values_by_field_by_artifact):
        success = self._login()
        if success:
            # Artifacts
            artifacts = Artifacts(self.connection)
            for values_by_field in values_by_field_by_artifact.values():
                success = artifacts.create_artifact(tracker_id, values_by_field)
                if success:
                    self.response = artifacts.get_data()
                else:
                    return False, self.response

            return True, self.response

        return False, self.response
