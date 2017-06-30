from Tuleap.RestClient.Commons import Order
from Tuleap.RestClient.Projects import Projects
from lib.base import BaseTuleapAction


class GetMilestones(BaseTuleapAction):
    def run(self, project_id, order):
        success = self._login()
        if success:
            # Projects
            projects = Projects(self.connection)
            if order == 'descending':
                success = projects.request_milestones(project_id, Order.Descending)
            else:
                success = projects.request_milestones(project_id, Order.Ascending)
            if success:
                self.response = projects.get_data()

                return True, self.response

        return False, self.response
