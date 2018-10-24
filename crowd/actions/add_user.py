from lib.base import CrowdBaseAction

class CrowdAddUserAction(CrowdBaseAction):
	def run(self, username, password, email):
		# Return True if the user exists in the Crowd application.
		if not self.status:
			msg = 'Application authentication Failed.'
			return(False, msg)
			
		date = {
			"password": password,
			"email": email
		}
		result = self.crowd.add_user(username, **data)
		
		if result:
			return(True, result)
		else:
			return(False, result)
