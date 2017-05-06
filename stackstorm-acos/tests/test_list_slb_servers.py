import mock

from acos_base_action_test_case import ACOSBaseActionTestCase
from ax_action_runner import AXActionRunner


class ListSLBServersTestCase(ACOSBaseActionTestCase):
    __test__ = True
    action_cls = AXActionRunner

    @mock.patch('acos_client.Client')
    def test_list_slb_servers(self, mock_client):
        action = self.get_action_instance(self._full_config)

        # set mock of action
        mock_action = mock.Mock()
        mock_action.slb.server.get.return_value = 'test-result'

        mock_client.return_value = mock_action

        # execute action
        params = {
            'api_version': 'v3.0',
            'object_path': 'slb.server',
            'action': 'get',
            'name': 'hoge',
        }
        result = action.run(**params)

        self.assertTrue(result[0])
        self.assertEqual(result[1], 'test-result')
