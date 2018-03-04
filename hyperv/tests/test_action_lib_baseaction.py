from activedirectory_base_action_test_case import ActiveDirectoryBaseActionTestCase
from run_cmdlet import RunCmdlet
from mock import patch
import json


class TestActionLibBaseAction(ActiveDirectoryBaseActionTestCase):
    __test__ = True
    action_cls = RunCmdlet

    def test_init(self):
        action = self.get_action_instance({})
        self.assertEqual(action.connection, None)

    def test_create_creds_spec(self):
        action = self.get_action_instance({})
        expected = {'connect': {'credential_name': "cred_name",
                                'username': "username",
                                'password': "password",
                                'required': True},
                    'cmdlet': {'credential_name': "cmdlet_cred",
                               'username': "cmdlet_username",
                               'password': "cmdlet_password",
                               'required': False}}
        connect = expected['connect']
        cmdlet = expected['cmdlet']
        creds_spec = action.create_creds_spec(credential_name=connect['credential_name'],
                                              username=connect['username'],
                                              password=connect['password'],
                                              cmdlet_credential_name=cmdlet['credential_name'],
                                              cmdlet_username=cmdlet['username'],
                                              cmdlet_password=cmdlet['password'])
        self.assertIsInstance(creds_spec, dict)
        self.assertEqual(creds_spec, expected)

    def test_resolve_creds_spec_from_config(self):
        action = self.get_action_instance(self.config_good)
        creds_spec = {'credential_name': 'base',
                      'required': True}
        resolved = action.resolve_creds_spec(creds_spec)
        expected = {'credential_name': 'base',
                    'username': self.config_good['activedirectory']['base']['username'],
                    'password': self.config_good['activedirectory']['base']['password']}
        self.assertIsInstance(resolved, dict)
        self.assertEqual(resolved, expected)

    def test_resolve_creds_spec_from_cmdline(self):
        action = self.get_action_instance(self.config_good)
        cmdline_creds = {'credential_name': '',
                         'username': 'cmdline-user',
                         'password': 'cmdline-pass'}
        creds_spec = {'credential_name': '',
                      'username': cmdline_creds['username'],
                      'password': cmdline_creds['password'],
                      'required': True}
        resolved = action.resolve_creds_spec(creds_spec)
        self.assertIsInstance(resolved, dict)
        self.assertEqual(resolved, cmdline_creds)

    def test_resolve_creds_spec_from_cmdline_override_config(self):
        action = self.get_action_instance(self.config_good)
        cmdline_creds = {'credential_name': 'base',
                         'username': 'cmdline-user',
                         'password': 'cmdline-pass'}
        creds_spec = {'credential_name': cmdline_creds['credential_name'],
                      'username': cmdline_creds['username'],
                      'password': cmdline_creds['password'],
                      'required': True}
        resolved = action.resolve_creds_spec(creds_spec)
        self.assertIsInstance(resolved, dict)
        self.assertEqual(resolved, cmdline_creds)

    def test_resolve_creds_spec_config_creds_missing(self):
        action = self.get_action_instance(self.config_good)
        creds_spec = {'credential_name': 'NONEXISTENT-CREDS-NAME',
                      'required': True}
        with self.assertRaises(KeyError):
            action.resolve_creds_spec(creds_spec)

    def test_resolve_creds_spec_config_creds_missing_username(self):
        action = self.get_action_instance(self.config_partial)
        creds_spec = {'credential_name': 'missing-username',
                      'required': True}
        with self.assertRaises(KeyError):
            action.resolve_creds_spec(creds_spec)

    def test_resolve_creds_spec_config_creds_missing_password(self):
        action = self.get_action_instance(self.config_partial)
        creds_spec = {'credential_name': 'missing-password',
                      'required': True}
        with self.assertRaises(KeyError):
            action.resolve_creds_spec(creds_spec)

    def test_resolve_creds_from_config(self):
        config = self.config_good
        action = self.get_action_instance(config)
        config_connect = config['activedirectory']['base']
        config_cmdlet = config['activedirectory']['tport-override']
        resolved = action.resolve_creds(credential_name='base',
                                        username=config_connect['username'],
                                        password=config_connect['password'],
                                        cmdlet_credential_name='tport-override',
                                        cmdlet_username=config_cmdlet['username'],
                                        cmdlet_password=config_cmdlet['password'])
        expected = {'connect': {'credential_name': 'base',
                                'username': config_connect['username'],
                                'password': config_connect['password']},
                    'cmdlet': {'credential_name': 'tport-override',
                               'username': config_cmdlet['username'],
                               'password': config_cmdlet['password'],
                               'port': config_cmdlet['port'],
                               'transport': config_cmdlet['transport']}}
        self.assertEqual(resolved, expected)

    def test_resolve_creds_from_cmdline(self):
        config = self.config_good
        action = self.get_action_instance(config)
        expected = {'connect': {'credential_name': '',
                                'username': 'cmdline-username',
                                'password': 'cmdline-password'},
                    'cmdlet': {'credential_name': '',
                               'username': 'cmdlet-cmdline-username',
                               'password': 'cmdlet-cmdline-password'}}
        resolved = action.resolve_creds(credential_name='',
                                        username=expected['connect']['username'],
                                        password=expected['connect']['password'],
                                        cmdlet_credential_name='',
                                        cmdlet_username=expected['cmdlet']['username'],
                                        cmdlet_password=expected['cmdlet']['password'])
        self.assertEqual(resolved, expected)

    def test_resolve_creds_from_cmdline_override_config(self):
        config = self.config_good
        action = self.get_action_instance(config)
        config_base = config['activedirectory']['base']
        expected = {'connect': {'credential_name': 'base',
                                'username': 'cmdline-username',
                                'password': config_base['password']},
                    'cmdlet': {'credential_name': 'base',
                               'username': config_base['username'],
                               'password': 'cmdlet-cmdline-password'}}
        resolved = action.resolve_creds(credential_name='base',
                                        username=expected['connect']['username'],
                                        password='',
                                        cmdlet_credential_name='base',
                                        cmdlet_username='',
                                        cmdlet_password=expected['cmdlet']['password'])
        self.assertEqual(resolved, expected)

    def test_resolve_transport_cmdline(self):
        action = self.get_action_instance(self.config_blank)
        expected = {'transport': 'abc', 'port': 123}
        connect_creds = {}
        resolved = action.resolve_transport(connect_creds,
                                            transport=expected['transport'],
                                            port=expected['port'])
        self.assertEqual(resolved, expected)

    def test_resolve_transport_config_creds(self):
        action = self.get_action_instance(self.config_good)
        config_tport = self.config_good['activedirectory']['tport-override']
        expected = {'transport': config_tport['transport'],
                    'port': config_tport['port']}
        creds = action.resolve_creds(credential_name='tport-override',
                                     username='',
                                     password='',
                                     cmdlet_credential_name='tport-override',
                                     cmdlet_username='',
                                     cmdlet_password='')
        resolved = action.resolve_transport(creds['connect'])
        self.assertEqual(resolved, expected)

    def test_resolve_transport_config_base(self):
        action = self.get_action_instance(self.config_good)
        config_tport = self.config_good
        expected = {'transport': config_tport['transport'],
                    'port': config_tport['port']}
        creds = action.resolve_creds(credential_name='base',
                                     username='',
                                     password='',
                                     cmdlet_credential_name='base',
                                     cmdlet_username='',
                                     cmdlet_password='')
        resolved = action.resolve_transport(creds['connect'])
        self.assertEqual(resolved, expected)

    def test_resolve_transport_default(self):
        action = self.get_action_instance(self.config_blank)
        expected = {'transport': action.default_transport(),
                    'port': action.default_port()}
        resolved = action.resolve_transport({})
        self.assertEqual(resolved, expected)

    def test_resolve_transport_kwargs_none(self):
        action = self.get_action_instance(self.config_good)
        config_tport = self.config_good
        expected = {'transport': config_tport['transport'],
                    'port': config_tport['port']}
        resolved = action.resolve_transport(expected, transport=None, port=None)
        self.assertEqual(resolved, expected)

    def get_output_ps_code(self, output):
        output_ps = ""
        if output == 'json':
            output_ps = ("Try\n"
                         "{{\n"
                         "  {0} | ConvertTo-Json\n"
                         "}}\n"
                         "Catch\n"
                         "{{\n"
                         "  $formatted_output = ConvertTo-Json -InputObject $_\n"
                         "  $host.ui.WriteErrorLine($formatted_output)\n"
                         "  exit 1\n"
                         "}}")
        elif output == 'csv':
            output_ps = ("Try\n"
                         "{{\n"
                         "  {0} | ConvertTo-Csv\n"
                         "}}\n"
                         "Catch\n"
                         "{{\n"
                         "  $formatted_output = ConvertTo-Csv -InputObject $_\n"
                         "  $host.ui.WriteErrorLine($formatted_output)\n"
                         "  exit 1\n"
                         "}}")
        elif output == 'xml':
            output_ps = ("Try\n"
                         "{{\n"
                         "  {0} | ConvertTo-Xml\n"
                         "}}\n"
                         "Catch\n"
                         "{{\n"
                         "  $formatted_output = ConvertTo-Xml -InputObject $_\n"
                         "  $host.ui.WriteErrorLine($formatted_output)\n"
                         "  exit 1\n"
                         "}}")
        else:
            output_ps = "{0}"
        return output_ps

    def test_resolve_output_ps_config(self):
        action = self.get_action_instance(self.config_good)
        expected = self.get_output_ps_code(self.config_good['output'])
        resolved = action.resolve_output_ps()
        self.assertEqual(resolved, expected)

    def test_resolve_output_ps_json(self):
        action = self.get_action_instance(self.config_blank)
        expected = self.get_output_ps_code('json')
        resolved = action.resolve_output_ps(output='json')
        self.assertEqual(resolved, expected)

    def test_resolve_output_ps_config_missing(self):
        action = self.get_action_instance(self.config_blank)
        with self.assertRaises(LookupError):
            action.resolve_output_ps()

    def test_resolve_output_ps_config_invalid(self):
        action = self.get_action_instance(self.config_partial)
        with self.assertRaises(LookupError):
            action.resolve_output_ps(output='invalid')

    @patch('lib.winrm_connection.WinRmConnection')
    def test_run_ad_cmdlet(self, connection):
        connection.run_ps.return_value.std_out = "cmdlet standard ouput"
        connection.run_ps.return_value.std_err = "cmdlet standard error"
        connection.run_ps.return_value.status_code = 0

        action = self.get_action_instance(self.config_good)
        action.connection = connection

        cmdlet = 'Test-Cmdlet'
        cmdlet_args = ''
        powershell = ("$ProgressPreference = 'SilentlyContinue';\n"
                      "{0} {1}").format(cmdlet, cmdlet_args)
        result = action.run_ad_cmdlet(cmdlet,
                                      credential_name='base',
                                      hostname='abc',
                                      output='raw')

        connection.run_ps.assert_called_with(powershell)

        self.assertEqual(result[0], True)
        self.assertEqual(result[1]['stdout'], connection.run_ps.return_value.std_out)
        self.assertEqual(result[1]['stderr'], connection.run_ps.return_value.std_err)
        self.assertEqual(result[1]['exit_status'], connection.run_ps.return_value.status_code)

    @patch('lib.winrm_connection.WinRmConnection')
    def test_run_ad_cmdlet_fail(self, connection):
        connection.run_ps.return_value.std_out = "cmdlet standard ouput"
        connection.run_ps.return_value.std_err = "cmdlet standard error"
        connection.run_ps.return_value.status_code = 1

        action = self.get_action_instance(self.config_good)
        action.connection = connection

        cmdlet = 'Test-Cmdlet'
        cmdlet_args = ''
        powershell = ("$ProgressPreference = 'SilentlyContinue';\n"
                      "{0} {1}").format(cmdlet, cmdlet_args)
        result = action.run_ad_cmdlet(cmdlet,
                                      credential_name='base',
                                      hostname='abc',
                                      output='raw')

        connection.run_ps.assert_called_with(powershell)

        self.assertEqual(result[0], False)
        self.assertEqual(result[1]['stdout'], connection.run_ps.return_value.std_out)
        self.assertEqual(result[1]['stderr'], connection.run_ps.return_value.std_err)
        self.assertEqual(result[1]['exit_status'], connection.run_ps.return_value.status_code)

    @patch('lib.winrm_connection.WinRmConnection')
    def test_run_ad_cmdlet_cmdlet_credentials(self, connection):
        connection.run_ps.return_value.std_out = "cmdlet standard ouput"
        connection.run_ps.return_value.std_err = "cmdlet standard error"
        connection.run_ps.return_value.status_code = 0

        action = self.get_action_instance(self.config_good)
        action.connection = connection

        cmdlet = 'Test-Cmdlet'
        cmdlet_args = ''
        powershell = ("$ProgressPreference = 'SilentlyContinue';\n"
                      "$securepass = ConvertTo-SecureString \"{3}\" -AsPlainText -Force;\n"
                      "$admincreds = New-Object System.Management.Automation.PSCredential(\"{2}\", $securepass);\n"  # noqa
                      "{0} -Credential $admincreds {1}"
                      "").format(cmdlet,
                                 cmdlet_args,
                                 self.config_good['activedirectory']['base']['username'],
                                 self.config_good['activedirectory']['base']['password'])
        result = action.run_ad_cmdlet(cmdlet,
                                      credential_name='base',
                                      cmdlet_credential_name='base',
                                      hostname='abc',
                                      output='raw')

        connection.run_ps.assert_called_with(powershell)

        self.assertEqual(result[0], True)
        self.assertEqual(result[1]['stdout'], connection.run_ps.return_value.std_out)
        self.assertEqual(result[1]['stderr'], connection.run_ps.return_value.std_err)
        self.assertEqual(result[1]['exit_status'], connection.run_ps.return_value.status_code)

    @patch('lib.winrm_connection.WinRmConnection')
    def test_run_ad_cmdlet_json(self, connection):
        connection.run_ps.return_value.std_out = "{\"cmdlet\": \"standard ouput\"}"
        connection.run_ps.return_value.std_err = "{\"cmdlet\": \"standard error\"}"
        connection.run_ps.return_value.status_code = 0

        action = self.get_action_instance(self.config_good)
        action.connection = connection

        cmdlet = 'Test-Cmdlet'
        cmdlet_args = ''
        powershell = "$ProgressPreference = 'SilentlyContinue';\n{0} {1}".format(cmdlet,
                                                                                 cmdlet_args)
        powershell = self.get_output_ps_code('json').format(powershell)
        result = action.run_ad_cmdlet(cmdlet,
                                      credential_name='base',
                                      hostname='abc',
                                      output='json')

        connection.run_ps.assert_called_with(powershell)

        self.assertEqual(result[0], True)
        self.assertEqual(result[1]['stdout'], connection.run_ps.return_value.std_out)
        self.assertEqual(result[1]['stderr'], connection.run_ps.return_value.std_err)
        self.assertEqual(result[1]['exit_status'], connection.run_ps.return_value.status_code)
        self.assertEqual(result[1]['stdout_dict'],
                         json.loads(connection.run_ps.return_value.std_out))
        self.assertEqual(result[1]['stderr_dict'],
                         json.loads(connection.run_ps.return_value.std_err))

    @patch('lib.winrm_connection.WinRmConnection')
    def test_run_ad_cmdlet_json_stdout_parse_fail(self, connection):
        connection.run_ps.return_value.std_out = "cmdlet standard ouput"
        connection.run_ps.return_value.std_err = "{\"cmdlet\": \"standard error\"}"
        connection.run_ps.return_value.status_code = 0

        action = self.get_action_instance(self.config_good)
        action.connection = connection

        cmdlet = 'Test-Cmdlet'
        with self.assertRaises(ValueError):
            action.run_ad_cmdlet(cmdlet,
                                 credential_name='base',
                                 hostname='abc',
                                 output='json')

    @patch('lib.winrm_connection.WinRmConnection')
    def test_run_ad_cmdlet_json_stderr_parse_fail(self, connection):
        connection.run_ps.return_value.std_out = "{\"cmdlet\": \"standard ouput\"}"
        connection.run_ps.return_value.std_err = "cmdlet standard error"
        connection.run_ps.return_value.status_code = 0

        action = self.get_action_instance(self.config_good)
        action.connection = connection

        cmdlet = 'Test-Cmdlet'
        with self.assertRaises(ValueError):
            action.run_ad_cmdlet(cmdlet,
                                 credential_name='base',
                                 hostname='abc',
                                 output='json')

    @patch('lib.winrm_connection.WinRmConnection')
    def test_run_ad_cmdlet_json_parse_empty(self, connection):
        connection.run_ps.return_value.std_out = ""
        connection.run_ps.return_value.std_err = ""
        connection.run_ps.return_value.status_code = 0

        action = self.get_action_instance(self.config_good)
        action.connection = connection

        cmdlet = 'Test-Cmdlet'
        cmdlet_args = ''
        powershell = "$ProgressPreference = 'SilentlyContinue';\n{0} {1}".format(cmdlet,
                                                                                 cmdlet_args)
        powershell = self.get_output_ps_code('json').format(powershell)
        result = action.run_ad_cmdlet(cmdlet,
                                      credential_name='base',
                                      hostname='abc',
                                      output='json')

        connection.run_ps.assert_called_with(powershell)

        self.assertEqual(result[0], True)
        self.assertEqual(result[1]['stdout'], connection.run_ps.return_value.std_out)
        self.assertEqual(result[1]['stderr'], connection.run_ps.return_value.std_err)
        self.assertEqual(result[1]['exit_status'], connection.run_ps.return_value.status_code)
        self.assertEqual(result[1]['stdout_dict'], {})
        self.assertEqual(result[1]['stderr_dict'], {})

    @patch('lib.winrm_connection.WinRmConnection')
    def test_run_ad_cmdlet_cmdlet_credentials_json(self, connection):
        connection.run_ps.return_value.std_out = "{\"cmdlet\": \"standard ouput\"}"
        connection.run_ps.return_value.std_err = "{\"cmdlet\": \"standard error\"}"
        connection.run_ps.return_value.status_code = 0

        action = self.get_action_instance(self.config_good)
        action.connection = connection

        cmdlet = 'Test-Cmdlet'
        cmdlet_args = ''
        powershell = ("$ProgressPreference = 'SilentlyContinue';\n"
                      "$securepass = ConvertTo-SecureString \"{3}\" -AsPlainText -Force;\n"
                      "$admincreds = New-Object System.Management.Automation.PSCredential(\"{2}\", $securepass);\n"  # noqa
                      "{0} -Credential $admincreds {1}"
                      "").format(cmdlet,
                                 cmdlet_args,
                                 self.config_good['activedirectory']['base']['username'],
                                 self.config_good['activedirectory']['base']['password'])
        powershell = self.get_output_ps_code('json').format(powershell)
        result = action.run_ad_cmdlet(cmdlet,
                                      credential_name='base',
                                      cmdlet_credential_name='base',
                                      hostname='abc',
                                      output='json')

        connection.run_ps.assert_called_with(powershell)

        self.assertEqual(result[0], True)
        self.assertEqual(result[1]['stdout'], connection.run_ps.return_value.std_out)
        self.assertEqual(result[1]['stderr'], connection.run_ps.return_value.std_err)
        self.assertEqual(result[1]['exit_status'], connection.run_ps.return_value.status_code)
        self.assertEqual(result[1]['stdout_dict'],
                         json.loads(connection.run_ps.return_value.std_out))
        self.assertEqual(result[1]['stderr_dict'],
                         json.loads(connection.run_ps.return_value.std_err))
