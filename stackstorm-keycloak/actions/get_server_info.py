from lib import action

class KeycloakGetServerInfoAction(action.KeycloakBaseAction):
    def run(self):

        return self.keycloak_admin.get_server_info()
