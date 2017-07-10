from men_and_mice_base_action_test_case import MenAndMiceBaseActionTestCase

from lib.run_login import RunLogin
from st2actions.runners.pythonrunner import Action

from mock import Mock, patch


class TestActionLibRunLogin(MenAndMiceBaseActionTestCase):
    __test__ = True
    action_cls = RunLogin

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, RunLogin)
        self.assertIsInstance(action, Action)

    @patch("lib.run_operation.RunOperation._pre_exec")
    def test_run(self, mock__pre_exec):
        action = self.get_action_instance(self.config_blank)
        connection = {'connection': None,
                      'username': 'user',
                      'password': 'pass',
                      'server': 'menandmice.domain.tld'}
        kwargs_dict = {'session': None,
                       'operation': "Login"}
        kwargs_dict.update(connection)
        context = {'connection': connection}
        expected_session = "xyz123"

        mock_client = Mock()
        mock_client.service.Login.return_value = expected_session

        mock__pre_exec.return_value = (context, mock_client)

        result = action.run(**kwargs_dict)

        mock_client.service.Login.assert_called_with(server=context['connection']['server'],
                                                     loginName=context['connection']['username'],
                                                     password=context['connection']['password'])

        self.assertEquals(result, {'session': expected_session})
