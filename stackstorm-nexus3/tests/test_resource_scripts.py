from st2tests.base import BaseActionTestCase

from run import ActionManager
from lib.exception import *
from lib.base import BaseAction
import mock
import json
from nexus_base_test_case import NexusBaseTestCase

@mock.patch('lib.base.NexusClient' )
class ResourceScriptsTest(NexusBaseTestCase):
    action_cls = ActionManager
    __test__ = True
    
    def test_action_list_scripts(self, mock_nexus):
        """ (A)List scripts: Should fetch an array of scripts
        """

        action_config = self.get_action_config("list_scripts")
        pack_config = self._configs["pack_config"]
        script_list_fixture = self.get_fixture_content('list_scripts.json')

        mock_client = mock_nexus.return_value
        mock_client.scripts.list.return_value = script_list_fixture

        action = self.get_action_instance(pack_config)
        (is_success, response) = action.run(**action_config)
        
        mock_client.scripts.list.assert_called_once()
        self.assertEqual(response, script_list_fixture)

    def test_action_get_scripts(self, mock_nexus):
        """ (A)Get scripts: Should fetch a script identified by name
        """

        action_config = self.get_action_config("get_scripts")
        pack_config = self._configs["pack_config"]
        script_fixture = self.get_fixture_content('get_scripts.json')

        def mock_get(name):
            return script_fixture

        mock_client = mock_nexus.return_value
        mock_client.scripts.get = mock.Mock(side_effect=mock_get)

        action = self.get_action_instance(pack_config)
        (is_success, response) = action.run(**action_config)

        mock_client.scripts.get.assert_called_once()
        self.assertEqual((is_success, response), (True, script_fixture))
        

    def test_action_create_scripts(self, mock_nexus):
        """ (A)Create scripts: Should create a script
        """

        action_config = self.get_action_config("create_scripts")
        pack_config = self._configs["pack_config"]

        def mock_create_if_missing(payload):
            return None

        mock_client = mock_nexus.return_value
        mock_client.scripts.create_if_missing = mock.Mock(side_effect=mock_create_if_missing)

        action = self.get_action_instance(pack_config)
        (is_success, response) = action.run(**action_config)

        mock_client.scripts.create_if_missing.assert_called_once()
        self.assertEqual((is_success, response), (True, None))


    def test_action_delete_scripts(self, mock_nexus):
        """ (A)delete scripts: Should delete a script
        """

        action_config = self.get_action_config("delete_scripts")
        pack_config = self._configs["pack_config"]

        def mock_delete(name):
            return None

        mock_client = mock_nexus.return_value
        mock_client.scripts.delete = mock.Mock(side_effect=mock_delete)

        action = self.get_action_instance(pack_config)
        (is_success, response) = action.run(**action_config)

        mock_client.scripts.delete.assert_called_once()
        self.assertEqual((is_success, response), (True, None))
        
        