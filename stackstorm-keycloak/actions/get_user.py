from lib import action

class KeycloakGetUserAction(action.KeycloakBaseAction):
    def run(self, username):

        user = self.keycloak_admin.get_user(username=username)
        return user
