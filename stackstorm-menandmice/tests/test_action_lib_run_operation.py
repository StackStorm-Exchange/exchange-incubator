from men_and_mice_base_action_test_case import MenAndMiceBaseActionTestCase

from lib.run_operation import RunOperation
from lib.run_operation import CONFIG_CONNECTION_KEYS
from st2actions.runners.pythonrunner import Action

import copy
import mock
import zeep
import logging


class TestActionLibRunOperation(MenAndMiceBaseActionTestCase):
    __test__ = True
    action_cls = RunOperation

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, RunOperation)
        self.assertIsInstance(action, Action)

    def test_snake_to_camel(self):
        action = self.get_action_instance({})
        snake = "snake_case_string"
        camel = "snakeCaseString"
        result = action.snake_to_camel(snake)
        self.assertEqual(result, camel)

    def test_get_del_arg_present(self):
        action = self.get_action_instance({})
        test_dict = {"key1": "value1",
                     "key2": "value2"}
        test_key = "key1"
        expected_dict = {"key2": "value2"}
        expected_value = test_dict["key1"]
        result_value = action.get_del_arg(test_key, test_dict)
        self.assertEqual(result_value, expected_value)
        self.assertEqual(test_dict, expected_dict)

    def test_get_del_arg_missing(self):
        action = self.get_action_instance({})
        test_dict = {"key1": "value1",
                     "key2": "value2"}
        test_key = "key3"
        expected_dict = test_dict
        expected_value = None
        result_value = action.get_del_arg(test_key, test_dict)
        self.assertEqual(result_value, expected_value)
        self.assertEqual(test_dict, expected_dict)

    def test_resolve_connection_from_config(self):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        connection_config = self.config_good['menandmice'][connection_name]
        connection_expected = {'connection': connection_name}
        connection_expected.update(connection_config)
        kwargs_dict = {'connection': connection_name}
        connection_result = action.resolve_connection(kwargs_dict)
        self.assertEqual(connection_result, connection_expected)

    def test_resolve_connection_from_config_missing(self):
        action = self.get_action_instance(self.config_good)
        connection_name = 'this_connection_doesnt_exist'
        kwargs_dict = {'connection': connection_name}
        with self.assertRaises(KeyError):
            action.resolve_connection(kwargs_dict)

    def test_resolve_connection_from_config_defaults(self):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        connection_expected = {'connection': connection_name}
        connection_expected.update(connection_config)
        for key, required, default in CONFIG_CONNECTION_KEYS:
            if not required and default:
                connection_expected[key] = default

        kwargs_dict = {'connection': connection_name}
        connection_result = action.resolve_connection(kwargs_dict)
        self.assertEqual(connection_result, connection_expected)

    def test_resolve_connection_from_kwargs(self):
        action = self.get_action_instance(self.config_blank)
        kwargs_dict = {'connection': None,
                       'server': 'kwargs_server',
                       'username': 'kwargs_username',
                       'password': 'kwargs_password',
                       'port': 123,
                       'transport': 'abc123',
                       'wsdl_endpoint': 'xxx?wsdl'}
        connection_expected = copy.deepcopy(kwargs_dict)
        connection_result = action.resolve_connection(kwargs_dict)
        self.assertEqual(connection_result, connection_expected)
        self.assertEqual(kwargs_dict, {})

    def test_resolve_connection_from_kwargs_defaults(self):
        action = self.get_action_instance(self.config_blank)
        kwargs_dict = {'connection': None,
                       'server': 'kwargs_server',
                       'username': 'kwargs_username',
                       'password': 'kwargs_password'}
        connection_expected = copy.deepcopy(kwargs_dict)
        for key, required, default in CONFIG_CONNECTION_KEYS:
            if not required and default:
                connection_expected[key] = default

        connection_result = action.resolve_connection(kwargs_dict)
        self.assertEqual(connection_result, connection_expected)
        self.assertEqual(kwargs_dict, {})

    def test_resolve_connection_from_kwargs_extras(self):
        action = self.get_action_instance(self.config_blank)
        connection_expected = {'connection': None,
                               'server': 'kwargs_server',
                               'username': 'kwargs_username',
                               'password': 'kwargs_password',
                               'port': 123,
                               'transport': 'abc123',
                               'wsdl_endpoint': 'xxx?wsdl'}
        kwargs_dict = copy.deepcopy(connection_expected)
        kwargs_extras = {"extra_key1": "extra_value1",
                         "extra_key2": 234}
        kwargs_dict.update(kwargs_extras)
        connection_result = action.resolve_connection(kwargs_dict)
        self.assertEqual(connection_result, connection_expected)
        self.assertEqual(kwargs_dict, kwargs_extras)

    def test_validate_connection(self):
        action = self.get_action_instance(self.config_blank)
        connection = {}
        for key, required, default in CONFIG_CONNECTION_KEYS:
            if required:
                connection[key] = "value_for_key_{}".format(key)

        result = action.validate_connection(connection)
        self.assertTrue(result)

    def test_validate_connection_missing_raises(self):
        action = self.get_action_instance(self.config_blank)
        connection = {}
        with self.assertRaises(KeyError):
            action.validate_connection(connection)

    def test_validate_connection_none_raises(self):
        action = self.get_action_instance(self.config_blank)
        connection = {}
        for key, required, default in CONFIG_CONNECTION_KEYS:
            connection[key] = None

        with self.assertRaises(KeyError):
            action.validate_connection(connection)

    def test_build_wsdl_url(self):
        action = self.get_action_instance({})
        connection = {'transport': 'https',
                      'server': 'menandmice.domain.tld',
                      'wsdl_endpoint': '_mmwebext/mmwebext.dll?wsdl'}
        expected_url = ("{0}://{1}/{2}?server=localhost".
                        format(connection['transport'],
                               connection['server'],
                               connection['wsdl_endpoint']))
        wsdl_url = action.build_wsdl_url(connection)
        self.assertEquals(wsdl_url, expected_url)

    def test_build_wsdl_url_port(self):
        action = self.get_action_instance({})
        connection = {'transport': 'https',
                      'server': 'menandmice.domain.tld',
                      'port': 8443,
                      'wsdl_endpoint': '_mmwebext/mmwebext.dll?wsdl'}
        expected_url = ("{0}://{1}:{2}/{3}?server=localhost".
                        format(connection['transport'],
                               connection['server'],
                               connection['port'],
                               connection['wsdl_endpoint']))
        wsdl_url = action.build_wsdl_url(connection)
        self.assertEquals(wsdl_url, expected_url)

    def test_build_wsdl_url_missing_server(self):
        action = self.get_action_instance({})
        connection = {'transport': 'https',
                      'port': 8443,
                      'wsdl_endpoint': '_mmwebext/mmwebext.dll?wsdl'}
        with self.assertRaises(RuntimeError):
            action.build_wsdl_url(connection)

    def test_login(self):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection = self.config_good['menandmice'][connection_name]

        expected_session = "expected_session"

        mock_client = mock.Mock()
        mock_client.service.Login.return_value = expected_session

        result = action.login(mock_client, connection)

        mock_client.service.Login.assert_called_with(server=connection['server'],
                                                     loginName=connection['username'],
                                                     password=connection['password'])
        self.assertEquals(result, expected_session)

    @mock.patch('lib.run_operation.zeep.Client')
    def test__pre_exec_kwargs(self, mock_client):
        action = self.get_action_instance(self.config_blank)
        kwargs_dict = {'operation': 'GetDNSViews',
                       'session': 'abc123',
                       'server': 'menandmice.domain.tld',
                       'username': 'user',
                       'password': 'pass'}
        kwargs_dict_extras = {'arg1': 'value1',
                              'arg2': 'value2'}
        kwargs_dict.update(kwargs_dict_extras)
        wsdl_url = ("http://{0}/_mmwebext/mmwebext.dll?wsdl?server=localhost"
                    .format(kwargs_dict['server']))
        mock_client.return_value = 'mock client'
        expected_context = {'kwargs_dict': kwargs_dict_extras,
                            'operation': kwargs_dict['operation'],
                            'session': kwargs_dict['session'],
                            'connection': {'connection': None,
                                           'server': kwargs_dict['server'],
                                           'username': kwargs_dict['username'],
                                           'password': kwargs_dict['password'],
                                           'transport': 'http',
                                           'wsdl_endpoint': '_mmwebext/mmwebext.dll?wsdl'},
                            'wsdl_url': wsdl_url}
        kwargs_dict_copy = copy.deepcopy(kwargs_dict)

        result_context, result_client = action._pre_exec(**kwargs_dict_copy)
        mock_client.assert_called_with(wsdl=wsdl_url)
        self.assertEquals(result_client, mock_client.return_value)
        self.assertEquals(result_context, expected_context)

    @mock.patch('lib.run_operation.zeep.Client')
    def test__pre_exec_config(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        kwargs_dict = {'operation': 'GetDNSViews',
                       'session': None,
                       'connection': connection_name}
        connection = self.config_good['menandmice'][connection_name]
        kwargs_dict.update(connection)
        connection['connection'] = connection_name
        kwargs_dict_extras = {'arg1': 'value1',
                              'arg2': 'value2'}
        kwargs_dict.update(kwargs_dict_extras)
        wsdl_url = ("{0}://{1}:{2}/_mmwebext/mmwebext.dll?wsdl?server=localhost"
                    .format(kwargs_dict['transport'],
                            kwargs_dict['server'],
                            kwargs_dict['port']))
        mock_client.return_value = 'mock client'
        expected_context = {'kwargs_dict': kwargs_dict_extras,
                            'operation': kwargs_dict['operation'],
                            'session': kwargs_dict['session'],
                            'connection': connection,
                            'wsdl_url': wsdl_url}
        kwargs_dict_copy = copy.deepcopy(kwargs_dict)

        result_context, result_client = action._pre_exec(**kwargs_dict_copy)
        mock_client.assert_called_with(wsdl=wsdl_url)
        self.assertEquals(result_client, mock_client.return_value)
        self.assertEquals(result_context, expected_context)

    def test__exec_session(self):
        action = self.get_action_instance(self.config_blank)
        expected_args = {'paramOneValue': 'value1',
                         'paramTwoValue': 'value2'}
        context = {'kwargs_dict': {'param_one_value': 'value1',
                                   'param_two_value': 'value2'},
                   'operation': 'GetDNSViews',
                   'session': 'abc123',
                   'connection': {'server': 'menandmice.domain.tld',
                                  'username': 'user',
                                  'password': 'pass'}}
        expected_result = "abc"
        mock_operation = mock.Mock()
        mock_operation.return_value = expected_result
        mock_client = mock.MagicMock()
        mock_client.service.Login.return_value = False
        mock_client.service.__getitem__.return_value = mock_operation

        result = action._exec(context, mock_client)

        self.assertFalse(mock_client.service.Login.called)
        mock_client.service.__getitem__.assert_called_with(context['operation'])
        mock_operation.assert_called_with(session=context['session'],
                                          **expected_args)
        self.assertEquals(result, expected_result)

    def test__exec_login(self):
        action = self.get_action_instance(self.config_blank)
        expected_args = {'paramOneValue': 'value1',
                         'paramTwoValue': 'value2'}
        context = {'kwargs_dict': {'param_one_value': 'value1',
                                   'param_two_value': 'value2'},
                   'operation': 'GetDNSViews',
                   'session': None,
                   'connection': {'server': 'menandmice.domain.tld',
                                  'username': 'user',
                                  'password': 'pass'}}
        expected_result = "abc"
        expected_session = "abc123"
        mock_operation = mock.Mock()
        mock_operation.return_value = expected_result
        mock_client = mock.MagicMock()
        mock_client.service.Login.return_value = expected_session
        mock_client.service.__getitem__.return_value = mock_operation

        result = action._exec(context, mock_client)

        mock_client.service.Login.assert_called_with(server=context['connection']['server'],
                                                     loginName=context['connection']['username'],
                                                     password=context['connection']['password'])
        mock_client.service.__getitem__.assert_called_with(context['operation'])
        mock_operation.assert_called_with(session=expected_session,
                                          **expected_args)
        self.assertEquals(result, expected_result)

    def test__exec_login_bad_connection(self):
        action = self.get_action_instance(self.config_blank)
        context = {'kwargs_dict': {'param_one_value': 'value1',
                                   'param_two_value': 'value2'},
                   'operation': 'GetDNSViews',
                   'session': None,
                   'connection': {'server': 'menandmice.domain.tld'}}
        mock_client = mock.Mock()
        with self.assertRaises(KeyError):
            action._exec(context, mock_client)

    def test__post_exec(self):
        logging.disable(logging.CRITICAL)
        action = self.get_action_instance(self.config_blank)
        client = zeep.Client(wsdl="./etc/menandmice_wsdl_2017_06_26.xml")
        expected = {"adForest": [{"ref": "abc123",
                                  "name": "forest_name",
                                  "catalogServer": None,
                                  "password": None,
                                  "readOnly": None,
                                  "userName": None}]}
        type_class = client.get_type('ns0:ArrayOfADForest')
        obj = type_class(adForest=[{'ref': expected['adForest'][0]['ref'],
                                    'name': expected['adForest'][0]['name']}])
        result = action._post_exec(obj)
        self.assertEquals(result, expected)

    @mock.patch("lib.run_operation.RunOperation._post_exec")
    @mock.patch("lib.run_operation.RunOperation._exec")
    @mock.patch("lib.run_operation.RunOperation._pre_exec")
    def test_run(self, mock__pre_exec, mock__exec, mock__post_exec):
        action = self.get_action_instance(self.config_blank)
        kwargs_dict = {'username': 'user',
                       'password': 'pass'}
        context = "context"
        client = "client"
        exec_result = "exec result"
        post_exec_result = "post exec result"

        mock__pre_exec.return_value = (context, client)
        mock__exec.return_value = exec_result
        mock__post_exec.return_value = post_exec_result

        result = action.run(**kwargs_dict)

        mock__pre_exec.assert_called_with(**kwargs_dict)
        mock__exec.assert_called_with(context, client)
        mock__post_exec.assert_called_with(exec_result)
        self.assertEquals(result, post_exec_result)
