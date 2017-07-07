from men_and_mice_base_action_test_case import MenAndMiceBaseActionTestCase

from lib.run_logout import RunLogout
from st2actions.runners.pythonrunner import Action

from mock import Mock, patch


class TestActionLibRunLogout(MenAndMiceBaseActionTestCase):
    __test__ = True
    action_cls = RunLogout

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, RunLogout)
        self.assertIsInstance(action, Action)

    @patch("lib.run_operation.RunOperation._pre_exec")
    def test_run(self, mock__pre_exec):
        action = self.get_action_instance(self.config_blank)
        expected_session = "xyz123"
        connection = {'connection': None,
                      'username': 'user',
                      'password': 'pass',
                      'server': 'menandmice.domain.tld'}
        kwargs_dict = {'session': expected_session,
                       'operation': "Logout"}
        kwargs_dict.update(connection)
        context = {'connection': connection,
                   'session': expected_session}

        mock_client = Mock()
        mock_client.service.Logout.return_value = None
        mock__pre_exec.return_value = (context, mock_client)

        result = action.run(**kwargs_dict)

        mock_client.service.Logout.assert_called_with(session=expected_session)

        self.assertEquals(result, None)
