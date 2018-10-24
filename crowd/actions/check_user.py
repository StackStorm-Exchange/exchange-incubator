from lib.base import CrowdBaseAction

class CrowdCheckUserAction(CrowdBaseAction):
	def run(self, username):
		# Return True if the user exists in the Crowd application.
		if self.status:
			result = self.crowd.user_exists(username)
			return(True, result)
		else:
			msg = 'Application authentication Failed.'
			return(False, msg)
