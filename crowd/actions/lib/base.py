import crowd
from st2common.runners.base_action import Action

class CrowdBaseAction(Action):

	def __init__(self, config):
		super(CrowdBaseAction, self).__init__(config)
		self.crowd = self._get_client()

		# Test that application can authenticate to Crowd.
		self.status = self.crowd.auth_ping()
	
	def _get_client(self):
		crowd_configs = self.config['crowd']
		app_url = crowd_configs['app_url']
		app_user = crowd_configs['app_user']
		app_pass = crowd_configs['app_pass']

		# Create the reusable Crowd object.
		client = crowd.CrowdServer(app_url, app_user, app_pass)
		return client
