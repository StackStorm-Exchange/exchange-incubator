from lib import action

class KeycloakUpdateUserAction(action.KeycloakBaseAction):
    def run(self, username, email='', firstName='', lastName='', enabled=True, emailVerified=False):
        user_id = self.keycloak_admin.get_user_id(username=username)
        if user_id != None:
            self.keycloak_admin.update_user(user_id=user_id, username=username, email=email, firstName=firstName, lastName=lastName, emailVerified=emailVerified, enabled=enabled)
        else:
            return "User " + username + " does not exist"
