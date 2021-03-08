from st2tests.base import BaseActionTestCase

from parse import SetupEntityAction

__all__ = ['SetupEntityActionTestCase']


class SetupEntityActionTestCase(BaseActionTestCase):
    action_cls = SetupEntityAction

    def test_run_setup_entities(self):
        result = self.get_action_instance().run()
        success = True
        self.assertEqual(result, expected)
