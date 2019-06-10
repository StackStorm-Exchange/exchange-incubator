from lib.actions import BaseAction


class ClusterInfoAction(BaseAction):

    def run(self):
        cluster_controller = self.client.cluster
        result = cluster_controller.get_basic_cluster_info()
        return (True, vars(result))
