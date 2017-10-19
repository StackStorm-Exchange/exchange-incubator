from lib import action

class KeycloakGetClientsAction(action.KeycloakBaseAction):
    def run(self):

        return self.keycloak_admin.get_clients()
