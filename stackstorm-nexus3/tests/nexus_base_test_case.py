from st2tests.base import BaseActionTestCase
import json

__all__ = [
    'NexusBaseTestCase'
]


class NexusBaseTestCase(BaseActionTestCase):
    __test__ = False
    action_cls = None

    def setUp(self):
        super(NexusBaseTestCase, self).setUp()

        self._configs = {
            "action_config": {
                "config_profile": None
            },
            "pack_config": {
                "url": "http://localhost:8081",
                "user": "user",
                "password": "supersecret"
            }
        }

    def get_action_config(self, action_name):
        self._configs["action_config"]["action"] = action_name

        if action_name in ["get_repositories", "delete_repositories",
                           "get_scripts", "delete_scripts"]:
            self._configs["action_config"]["name"] = "maven2-repo"
        elif action_name == "create_repositories":
            self._configs["action_config"].update(json.loads(
                self.get_fixture_content('get_repositories.json')))

        return self._configs["action_config"]

    def get_pack_config(self):
        return self._configs['pack_config']
