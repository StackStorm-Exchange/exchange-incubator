from run import ActionManager
import mock
from nexus_base_test_case import NexusBaseTestCase
from lib.exception import UnsupportedActionOrResourceError


@mock.patch('lib.base.NexusClient')
class ResourceUnsupportedTest(NexusBaseTestCase):
    action_cls = ActionManager
    __test__ = True

    def test_unsupported_resource(self, mock_nexus):
        """ Resource Or Action unsupported: Should raise exception
        """

        action_config = self.get_action_config("unsupported_resource")
        pack_config = self._configs["pack_config"]

        # aciton name in right format but still unsupported
        action = self.get_action_instance(pack_config)
        with self.assertRaises(UnsupportedActionOrResourceError):
            action.run(**action_config)

        # action name in invalid format
        action_config = self.get_action_config("unsupported")
        with self.assertRaises(UnsupportedActionOrResourceError):
            action.run(**action_config)
