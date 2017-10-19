from lib import action

class KeycloakgetUserIdAction(action.KeycloakBaseAction):
    def run(self, username):

        user_id = self.keycloak_admin.get_user_id(username=username)
        return user_id
