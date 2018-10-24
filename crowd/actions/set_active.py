from lib.base import CrowdBaseAction

class CrowdSetActiveAction(CrowdBaseAction):
	def run(self, username, active_state):
		# Return True if the user exists in the Crowd application.
		if not self.status:
			msg = 'Application authentication Failed.'
			return(False, msg)
			
		result = self.crowd.set_active(username, active_state)
		
		if result is None:
			return(False, result)
		else:
			return(True, result)
