from lib import action

class KeycloakgetClientAction(action.KeycloakBaseAction):
    def run(self, client_id):

        client = self.keycloak_admin.get_client(client_id=client_id)
        return client
