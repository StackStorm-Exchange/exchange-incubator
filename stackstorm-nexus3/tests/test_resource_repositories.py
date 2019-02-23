from st2tests.base import BaseActionTestCase

from run import ActionManager
from lib.exception import *
from lib.base import BaseAction
import mock
import json
from nexus_base_test_case import NexusBaseTestCase

@mock.patch('lib.base.NexusClient' )
class ResourceRepositoriesTest(NexusBaseTestCase):
    action_cls = ActionManager
    __test__ = True
    
    def test_action_list_repositories(self, mock_nexus):
        """ (A)List Repositories: Should fetch an array of repositories
        """

        action_config = self.get_action_config("list_repositories")
        pack_config = self._configs["pack_config"]
        repo_list_fixture = json.loads(self.get_fixture_content('list_repositories.json'))

        mock_client = mock_nexus.return_value
        mock_client.repositories.raw_list.return_value = repo_list_fixture

        action = self.get_action_instance(pack_config)
        (is_success, response) = action.run(**action_config)
        
        mock_client.repositories.raw_list.assert_called_once()
        self.assertEqual(response, repo_list_fixture)

    def test_action_get_repositories(self, mock_nexus):
        """ (A)Get Repositories: Should fetch a repository identified by a name
        """

        action_config = self.get_action_config("get_repositories")
        pack_config = self._configs["pack_config"]
        repository_fixture = json.loads(self.get_fixture_content('get_repositories.json'))

        def mock_get_raw_by_name(name):
            return repository_fixture

        mock_client = mock_nexus.return_value
        mock_client.repositories.get_raw_by_name = mock.Mock(side_effect=mock_get_raw_by_name)

        action = self.get_action_instance(pack_config)
        (is_success, response) = action.run(**action_config)

        mock_client.repositories.get_raw_by_name.assert_called_once()
        self.assertEqual((is_success, response), (True, repository_fixture))
        

    def test_action_create_repositories(self, mock_nexus):
        """ (A)Create Repositories: Should create a repository
        """

        action_config = self.get_action_config("create_repositories")
        pack_config = self._configs["pack_config"]

        def mock_create(payload):
            return None

        mock_client = mock_nexus.return_value
        mock_client.repositories.create = mock.Mock(side_effect=mock_create)

        action = self.get_action_instance(pack_config)
        (is_success, response) = action.run(**action_config)

        mock_client.repositories.create.assert_called_once()
        self.assertEqual((is_success, response), (True, None))


    def test_action_delete_repositories(self, mock_nexus):
        """ (A)Delete Repositories: Should delete a repository
        """

        action_config = self.get_action_config("delete_repositories")
        pack_config = self._configs["pack_config"]

        def mock_delete(name):
            return None

        mock_client = mock_nexus.return_value
        mock_client.repositories.delete = mock.Mock(side_effect=mock_delete)

        action = self.get_action_instance(pack_config)
        (is_success, response) = action.run(**action_config)

        mock_client.repositories.delete.assert_called_once()
        self.assertEqual((is_success, response), (True, None))
        
        