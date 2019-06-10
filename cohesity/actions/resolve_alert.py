from lib.actions import BaseAction
from cohesity_management_sdk.models.create_alert_resolution_request import \
    CreateAlertResolutionRequest
from cohesity_management_sdk.models.alert_resolution_info import \
    AlertResolutionInfo


class ResolveAlertAction(BaseAction):

    def run(self, alert_id, summary, description):
        alerts_controller = self.client.alerts

        body = CreateAlertResolutionRequest()
        body.alert_id_list = [alert_id]
        body.resolution_details = AlertResolutionInfo()
        body.resolution_details.resolution_details = summary
        body.resolution_details.resolution_summary = description

        result = alerts_controller.create_resolution(body)
        return (True, vars(result))
