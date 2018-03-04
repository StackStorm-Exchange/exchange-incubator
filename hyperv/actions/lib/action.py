from winrm_connection import WinRmConnection
from st2common.runners.base_action import Action
import json

# Note:  in order for this to work you need to run the following script on the
# host
#  https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1

CREDENTIALS_ITEMS = ['username', 'password']
TRANSPORT_ITEMS = ['port', 'transport']


class BaseAction(Action):

    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(BaseAction, self).__init__(config)
        self.connection = None

    def resolve_creds(self, **kwargs):
        """Parses and resolves connection credentials (creds) from kwargs that
        were passed in as parameters to the action.
        :returns: A dict containing the 'connect' and 'cmdlet' credentials to
        use for this action execution
        """
        creds_config = self.create_creds_spec(**kwargs)
        creds = {}
        for key, value in creds_config.items():
            creds[key] = self.resolve_creds_spec(value)
        return creds

    def get_arg(self, key, **kwargs):
        """Attempts to retrieve an argument from kwargs with key.
        :param key: the key of the argument to retrieve from kwargs
        :returns: The value of key in kwargs, if it exists, otherwise None
        """
        if key in kwargs:
            return kwargs[key]
        else:
            return None

    def create_creds_spec(self, **kwargs):
        """Creates two credentials specification from all of the values in
        kwargs, one spec for 'connection', the other for 'cmdlet'.
        :returns: a dict of an initialized credentials spec from kwargs
        """
        return {'connect': {'credential_name': self.get_arg('credential_name', **kwargs),
                            'username': self.get_arg('username', **kwargs),
                            'password': self.get_arg('password', **kwargs),
                            'required': True},
                'cmdlet': {'credential_name': self.get_arg('cmdlet_credential_name', **kwargs),
                           'username': self.get_arg('cmdlet_username', **kwargs),
                           'password': self.get_arg('cmdlet_password', **kwargs),
                           'required': False}}

    def resolve_creds_spec(self, creds_spec):
        """Takes a credentials sepcification and attempts to lookup varaibles
        given the following order:

        1) If they are set in the incoming creds_spec, meaning they were given
        as an action parameter
        2) Lookup the variable from the 'credential_name' value
        :param creds_spec: dict of the credentials spec for this login.
        :returns: a credentials spec dict that has been resolved given the order
        """
        creds = {}

        # if the user specified the "credential_name" parameter
        # then grab the credentials from the pack's config.yaml
        credential_name = creds_spec['credential_name']
        config_creds = None
        if credential_name:
            config_creds = self.config['hyperv'].get(credential_name)
            if not config_creds:
                raise KeyError("config.yaml missing credential: hyperv:%s"
                               % credential_name)

        creds['credential_name'] = credential_name

        # Override the items in creds read in from the config given the
        # override parameters from the action itself
        # Example:
        #   'username' parameter on the action will override the username
        #   from the credential. This is useful for runnning the action
        #   standalone and/or from the commandline
        for item in CREDENTIALS_ITEMS:
            if item in creds_spec and creds_spec[item]:
                # use creds from cmdline first (override)
                creds[item] = creds_spec[item]
            elif config_creds and item in config_creds and config_creds[item]:
                # fallback to creds in config
                creds[item] = config_creds[item]

            # ensure that creds has all items (if this credential is required)
            if ('required' in creds_spec and creds_spec['required'] and item not in creds):
                if credential_name:
                    raise KeyError("config.yaml mising: hyperv:%s:%s"
                                   % (credential_name, item))
                else:
                    raise KeyError("missing action parameter %s" % item)

        # copy in all transport items into the credentials spec
        for item in TRANSPORT_ITEMS:
            if config_creds and item in config_creds and config_creds[item]:
                creds[item] = config_creds[item]

        return creds

    @staticmethod
    def default_transport():
        """ Returns the default transport for this WinRM connection
        :returns: 'ntlm'
        """
        return 'ntlm'

    @staticmethod
    def default_port():
        """ Returns the default port for this WinRM connection
        :returns: '5986'
        """
        return 5986

    def resolve_transport(self, connect_creds, **kwargs):
        """ Resolves the transport and port to use for the connection
        based on the following priorities:
        1) if port/transport specified as action params, use this
        2) if port/transport specified as params on the credentials in config
        3) if port/transport specified at root level in the config
        4) else, use the default port/transport (5986/ntlm)
        :param connect_creds: the connection credentials read in from the
        config.
        :returns: dictionary with 'transport' and 'port' set the resolved
        values
        :rtype: dictionary
        """
        resolved_transport = None
        resolved_port = None

        if 'port' in kwargs and kwargs['port']:
            resolved_port = kwargs['port']
        elif 'port' in connect_creds and connect_creds['port']:
            resolved_port = connect_creds['port']
        elif 'port' in self.config and self.config['port']:
            resolved_port = self.config['port']
        else:
            resolved_port = BaseAction.default_port()

        if 'transport' in kwargs and kwargs['transport']:
            resolved_transport = kwargs['transport']
        elif 'transport' in connect_creds and connect_creds['transport']:
            resolved_transport = connect_creds['transport']
        elif 'transport' in self.config and self.config['transport']:
            resolved_transport = self.config['transport']
        else:
            resolved_transport = BaseAction.default_transport()

        return {'transport': resolved_transport, 'port': resolved_port}

    def connect(self, hostname, transport, creds):
        """Connects to hostname given the transport authentication method and
        creds for login. If the connection is successful it is cached locally
        as self.connection and reused for all commands run via run_hyperv_cmdlet().
        :param hostname: Hostname to connect to
        :param transport: Authentication method to use aka "transport" (WinRM terminology)
        :param creds: Credentials to use for the connection
        """
        if not self.connection:
            self.connection = WinRmConnection(hostname=hostname,
                                              port=transport['port'],
                                              transport=transport['transport'],
                                              username=creds['username'],
                                              password=creds['password'])

    def resolve_output_ps(self, **kwargs):
        """Generates powershell code for the output format selected by
        the action (if specified as a param, otherwise looked up in config).
        :returns: a string (potentially empty) containing powershell code
        that will format the output to the appropriate format.
        """
        output_ps = ""
        output = self.get_arg('output', **kwargs)
        from_config = False
        if not output:
            if 'output' in self.config:
                output = self.config['output']
                from_config = True
            else:
                raise LookupError("'output' parameter not found on action AND "
                                  "'output' option is missing in config!")

        # @note not using Write-Error here because it prints out the full
        # error object instead of just the message to stdout (this screws
        # up our parsing from JSON).
        # Instead we use a method found here to utilizes another function
        # to write just a string to stderr
        # https://stackoverflow.com/questions/4998173/how-do-i-write-to-standard-error-in-powershell/15669365#15669365
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
        elif output == 'raw':
            output_ps = "{0}"
        else:
            if from_config:
                raise LookupError("Unknown 'output' type [{0}] from config "
                                  "(valid = json, raw)".format(output))
            else:
                raise LookupError("Unknown 'output' type [{0}] from action parameter "
                                  "(valid = json, raw)".format(output))

        return output_ps

    def parse_output(self, output_str, **kwargs):
        parsed_output = {}
        if not output_str:
            return parsed_output

        output = self.get_arg('output', **kwargs)
        from_config = False
        if not output:
            if 'output' in self.config:
                output = self.config['output']
                from_config = True
            else:
                raise LookupError("'output' parameter not found on action AND "
                                  "'output' option is missing in config!")

        if output == 'json':
            parsed_output = json.loads(output_str)
        elif output == 'raw':
            parsed_output = {}
        else:
            if from_config:
                raise LookupError("Unknown 'output' type [{0}] from config "
                                  "(valid = json, raw)".format(output))
            else:
                raise LookupError("Unknown 'output' type [{0}] from action parameter "
                                  "(valid = json, raw)".format(output))

        return parsed_output

    def run_hyperv_cmdlet(self, cmdlet, **kwargs):
        """Runs an Hyper-V cmdlet on a remote host.
        :param cmdlet: cmdlet to execut on remote host
        """
        creds = self.resolve_creds(**kwargs)
        tport = self.resolve_transport(creds['connect'], **kwargs)

        """Added $ProgressPreference = 'SilentlyContinue' as first line
        because if powershell attempts to load any modules
        the progress of the module loading is then forwarded
        into stderr and causes stackstorm to fail the call.
        There is an open pull request to pywinrm:
        https://github.com/diyan/pywinrm/issues/169
        """
        powershell = "$ProgressPreference = 'SilentlyContinue';\n"
        cmdlet_args = kwargs['args'] if 'args' in kwargs else ''
        output_ps = self.resolve_output_ps(**kwargs)

        if 'username' in creds['cmdlet'] and 'password' in creds['cmdlet']:
            powershell += ("$securepass = ConvertTo-SecureString \"{3}\" -AsPlainText -Force;\n"
                          "$admincreds = New-Object System.Management.Automation.PSCredential(\"{2}\", $securepass);\n"  # noqa
                          "{0} -Credential $admincreds {1}"
                          "").format(cmdlet,
                                     cmdlet_args,
                                     creds['cmdlet']['username'],
                                     creds['cmdlet']['password'])
        else:
            powershell += '{0} {1}'.format(cmdlet, cmdlet_args)

        # add output formatters to the powershell code
        powershell = output_ps.format(powershell)

        # connect to server
        self.connect(kwargs['hostname'], tport, creds['connect'])

        # run powershell command
        ps_result = self.connection.run_ps(powershell)
        result = {'stdout': ps_result.std_out,
                  'stderr': ps_result.std_err,
                  'exit_status': ps_result.status_code,
                  'stdout_dict': self.parse_output(ps_result.std_out, **kwargs),
                  'stderr_dict': self.parse_output(ps_result.std_err, **kwargs)}

        if result['exit_status'] == 0:
            return (True, result)
        else:
            return (False, result)
