from st2tests.base import BaseActionTestCase

from run import ActionManager
from lib.exception import *

class RunTestCase(BaseActionTestCase):
    action_cls = ActionManager

    def test_run_required_params(self):
        action = self.get_action_instance(config={'config_profile': 'dev'})
        #self.assertRaises(MissingParameterError,action.run)
        