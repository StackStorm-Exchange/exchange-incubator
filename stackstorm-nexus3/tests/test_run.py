from st2tests.base import BaseActionTestCase

from run import ActionManager
from lib.exception import *


class RunTestCase(BaseActionTestCase):
    action_cls = ActionManager

    def test_configuration(self):
        """ This tests action and pack configuration
        """
        configs = {
            "action_config": {
                "config_profile": None
            },
            "pack_config": {}
        }
        # Action should have required 'action' parameter
        action = self.get_action_instance(config=configs["pack_config"])
        with self.assertRaises(MissingParameterError):
            action.run(**configs["action_config"])

        # Profile should exist, if defined in action
        configs = {
            "action_config": {
                "action": "some_action",
                "url": "http://localhost:8080",
                "config_profile": "dev"
            },
            "pack_config": {}
        }
        action = self.get_action_instance(config=configs["pack_config"])
        with self.assertRaises(MissingProfileError):
            action.run(**configs["action_config"])

        # Required connection parameters should exist: url, user, password
        configs = {
            "action_config": {
                "action": "some_action",
                "url": "http://localhost:8080"
            },
            "pack_config": {}
        }
        action = self.get_action_instance(config=configs["pack_config"])
        with self.assertRaises(ValidationFailError):
            action.run(**configs["action_config"])
