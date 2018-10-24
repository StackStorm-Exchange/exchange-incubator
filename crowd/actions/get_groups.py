from lib.base import CrowdBaseAction

class CrowdGetGroupsAction(CrowdBaseAction):
	def run(self, username):
		# Return True if the user exists in the Crowd application.
		if not self.status:
			msg = 'Application authentication Failed.'
			return(False, msg)
			
		result = self.crowd.get_groups(username)
		
		if result is None:
			return(False, result)
		else:
			return(True, result)
