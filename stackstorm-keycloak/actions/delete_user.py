from lib import action

class KeycloakDeleteUserAction(action.KeycloakBaseAction):
    def run(self, user_id):

        self.keycloak_admin.delete_user(user_id=user_id)
