from lib.base import CrowdBaseAction

class CrowdAddUserToGroupAction(CrowdBaseAction):
	def run(self, username, groupname):
		# Return True if the user exists in the Crowd application.
		if not self.status:
			msg = 'Application authentication Failed.'
			return(False, msg)
			
		result = self.crowd.add_user_to_group(username, groupname)
		
		if result:
			return(True, result)
		else:
			return(False, result)
