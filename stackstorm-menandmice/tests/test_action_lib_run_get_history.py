from men_and_mice_base_action_test_case import MenAndMiceBaseActionTestCase

from lib.run_get_history import RunGetHistory
from st2actions.runners.pythonrunner import Action

from mock import Mock, patch

import copy


class TestActionLibRunGetHistory(MenAndMiceBaseActionTestCase):
    __test__ = True
    action_cls = RunGetHistory

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, RunGetHistory)
        self.assertIsInstance(action, Action)

    @patch("lib.run_operation.RunOperation._pre_exec")
    def test__pre_exec(self, mock__pre_exec):
        action = self.get_action_instance(self.config_blank)
        history_user = 'test_user'
        kwargs_dict = {'user_name': history_user}
        context = {'kwargs_dict': copy.deepcopy(kwargs_dict)}
        expected_context = {'kwargs_dict': {'username': history_user}}

        mock_client = Mock()
        mock__pre_exec.return_value = (context, mock_client)

        (result_context, result_client) = action._pre_exec(**kwargs_dict)

        mock__pre_exec.assert_called_with(**kwargs_dict)
        self.assertEquals(result_context, expected_context)
        self.assertEquals(result_client, mock_client)
