from lib import action

class KeycloakgetRolesAction(action.KeycloakBaseAction):
    def run(self):

        return self.keycloak_admin.get_roles()
