from lib.base import CrowdBaseAction

class CrowdSetAttributeAction(CrowdBaseAction):
	def run(self, username, attribute, value):
		# Return True if the user exists in the Crowd application.
		if not self.status:
			msg = 'Application authentication Failed.'
			return(False, msg)
			
		result = self.crowd.set_user_attribute(username, attribute, value)
		
		if result:
			return(True, result)
		else:
			return(False, result)
