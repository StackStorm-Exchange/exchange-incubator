import acos_client
import re

from acos_base_action_test_case import ACOSBaseActionTestCase
from ax_action_runner import AXActionRunner


class ActionInitializationTestCase(ACOSBaseActionTestCase):
    __test__ = True
    action_cls = AXActionRunner

    def setUp(self):
        super(ActionInitializationTestCase, self).setUp()

        self._action = self.get_action_instance(self._full_config)
        self._action.logger.addHandler(self._log_handler)

    def test_specify_version_30_without_error(self):
        # confirm to set AXAPI_30
        self.assertEqual(self._action.login(3.0)._version, acos_client.AXAPI_30)
        self.assertEqual(self._action.login('3.0')._version, acos_client.AXAPI_30)
        self.assertEqual(self._action.login('V3.0')._version, acos_client.AXAPI_30)
        self.assertEqual(self._action.login('ver3.0')._version, acos_client.AXAPI_30)
        self.assertEqual(self._action.login('version-3.0')._version, acos_client.AXAPI_30)

        self.assertEqual(self._log_handler.messages['warning'], [])
        self.assertEqual(self._log_handler.messages['error'], [])

    def test_specify_version_21_without_error(self):
        # confirm to set AXAPI_21
        self.assertEqual(self._action.login(2.1)._version, acos_client.AXAPI_21)
        self.assertEqual(self._action.login('2.1')._version, acos_client.AXAPI_21)
        self.assertEqual(self._action.login('V2.1')._version, acos_client.AXAPI_21)
        self.assertEqual(self._action.login('ver2.1')._version, acos_client.AXAPI_21)
        self.assertEqual(self._action.login('version-2.1')._version, acos_client.AXAPI_21)

        self.assertEqual(self._log_handler.messages['warning'], [])
        self.assertEqual(self._log_handler.messages['error'], [])

    def test_specify_unsupported_version(self):
        # confirm to set default api version when specify invalid one
        self.assertEqual(self._action.login('3.1')._version, acos_client.AXAPI_30)
        self.assertEqual(self._action.login('21')._version, acos_client.AXAPI_30)
        self.assertEqual(self._action.login('hoge')._version, acos_client.AXAPI_30)
        self.assertEqual(self._action.login(None)._version, acos_client.AXAPI_30)

        # check to output warning for each case
        self.assertEqual(len(self._log_handler.messages['warning']), 4)
        self.assertTrue(re.match(r'^This uses default API version.*',
                                 self._log_handler.messages['warning'][0]))
