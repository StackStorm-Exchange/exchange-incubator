from lib import action

class KeycloakGetClientRolesAction(action.KeycloakBaseAction):
    def run(self, client_id):

        client_roles = self.keycloak_admin.get_client_roles(client_id=client_id)
        return client_roles
