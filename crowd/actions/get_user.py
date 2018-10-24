from lib.base import CrowdBaseAction

class CrowdGetUserAction(CrowdBaseAction):
	def run(self, username):
		# Return True if the user exists in the Crowd application.
		if not self.status:
			msg = 'Application authentication Failed.'
			return(False, msg)
			
		result = self.crowd.get_user(username)
		
		if result is None:
			return(False, result)
		else:
			return(True, result)
