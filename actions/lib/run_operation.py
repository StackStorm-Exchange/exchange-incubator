from st2actions.runners.pythonrunner import Action

import zeep
import re

#                         (key, required, default)
CONFIG_CONNECTION_KEYS = [('server', True, ""),
                          ('username', True, ""),
                          ('password', True, ""),
                          ('port', False, ""),
                          ('transport', False, "http")]

class RunOperation(Action):

    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(RunOperation, self).__init__(config)
        self._first_cap_re = re.compile(r'(.)([A-Z][a-z]+)')
        self._all_cap_re   = re.compile('([a-z0-9])([A-Z])')

    def camel_to_snake(self, camel_cased_str):
        """
        This function converts to snake_case from camelCase
        """
        sub1            = self._first_cap_re.sub(r'\1_\2', camel_cased_str)
        snake_cased_str = self._all_cap_re.sub(r'\1_\2', sub1).lower()
        return snake_cased_str.replace('__', '_')

    def camel_to_dash(self, camel_cased_str):
        """
        This function converts to dashed_case from camelCase
        """
        sub2            = self._first_cap_re.sub(r'\1-\2', camel_cased_str)
        dashed_case_str = self._all_cap_re.sub(r'\1-\2', sub2).lower()
        return dashed_case_str.replace('--', '-')

    def snake_to_camel(self, snake_cased_str):
        return self._convert_to_camel(snake_cased_str, "_")

    def dash_to_camel(self, snake_cased_str):
        return self._convert_to_camel(snake_cased_str, "-")

    def _convert_to_camel(self, snake_cased_str, separator):
        components = snake_cased_str.split(separator)
        preffix    = ""
        suffix     = ""
        if components[0] == "":
            components = components[1:]
            preffix    = separator
        if components[-1] == "":
            components = components[:-1]
            suffix     = separator
        if len(components) > 1:
            camel_cased_str = components[0].lower()
            for x in components[1:]:
                if x.isupper() or x.istitle():
                    camel_cased_str += x
                else:
                    camel_cased_str += x.title()
        else:
            camel_cased_str = components[0]
        return preffix + camel_cased_str + suffix

    def get_del_arg(self, key, kwargs_dict):
        """Attempts to retrieve an argument from kwargs with key.
        If the key is found, then delete it from the dict.
        :param key: the key of the argument to retrieve from kwargs
        :returns: The value of key in kwargs, if it exists, otherwise None
        """
        if key in kwargs_dict:
            value = kwargs_dict[key]
            del kwargs_dict[key]
            return value
        else:
            return None

    def resolve_connection(self, kwargs_dict):
        connection_name = self.get_del_arg('connection', kwargs_dict)
        config_connection = None
        if connection_name:
            config_connection = self.config['menandmice'].get(connection_name)
            if not config_creds:
                raise KeyError("config.yaml missing connection: menandmice:{0}"
                               .format(connection_name))

        action_connection = {'connection': connection_name}

        # Override the keys in creds read in from the config given the
        # override parameters from the action itself
        # Example:
        #   'username' parameter on the action will override the username
        #   from the credential. This is useful for runnning the action
        #   standalone and/or from the commandline
        for key, required, default in CONFIG_CONNECTION_KEYS:
            if key in kwargs_dict and kwargs_dict[key]:
                # use params from cmdline first (override)
                action_connection[key] = self.get_del_arg(key, kwargs_dict)
            elif config_connection and key in config_connection and config_connection[key]:
                # fallback to creds in config
                action_connection[key] = config_connection[key]
            else:
                if not required and default:
                    action_connection[key] = default

            # remove the key from kwargs if it's still in there
            if key in kwargs_dict:
                del kwargs_dict[key]

        return action_connection

    def validate_connection(self, connection):
        for key, required, default in CONFIG_CONNECTION_KEYS:
            if key in connection and connection[key]:
                continue
            else:
                if not required:
                    continue
                elif connection['connection']:
                    raise KeyError("config.yaml mising: menandmice:{0}:{1}"
                                   .format(connection['connection'], key))
                else:
                    raise KeyError("Because the 'connection' action parameter was"
                                   " not specified, the following action parameter"
                                   " is required: {0}".format(key))
        return True

    def build_wsdl_url(self, connection):
        wsdl_url = None
        if 'port' in connection and connection['port']:
            url_str = "{0}://{1}:{2}/_mmwebext/mmwebext.dll?wsdl?server=localhost"
            wsdl_url = url_str.format(connection['transport'],
                                      connection['server'],
                                      connection['port'])
        else:
            url_str = "{0}://{1}/_mmwebext/mmwebext.dll?wsdl?server=localhost"
            wsdl_url = url_str.format(connection['transport'],
                                      connection['server'])

        return wsdl_url

    def run(self, **kwargs):
        kwargs_dict = dict(kwargs)
        connection = self.resolve_connection(kwargs_dict)
        wsdl_url = self.build_wsdl_url(connection)
        client = zeep.Client(wsdl=wsdl_url)

        operation = self.get_del_arg('operation', kwargs_dict)
        session = self.get_del_arg('session', kwargs_dict)

        # username parameter was renamed in generate because
        # it conflicted with the username from the connection
        # undo that rename here so it's passed properly
        if operation == 'GetHistory':
            kwargs_dict['username'] = kwargs_dict['user_name']
            del kwargs_dict['user_name']

        if operation == 'Logout':
            # don't validate connection info for logout because
            # most of the connection parameters are not needed
            result = client.service.Logout(session=session)
            result_dict = zeep.helpers.serialize_object(result)
        elif operation == 'Login':
            # special handler for login to map parameter names
            self.validate_connection(connection)
            session = client.service.Login(server=connection['server'],
                                           loginName=connection['username'],
                                           password=connection['password'])
            result_dict = {'session': session}
        else:
            self.validate_connection(connection)
            if not session:
                session = client.service.Login(server=connection['server'],
                                               loginName=connection['username'],
                                               password=connection['password'])

            op_args = {}
            for snake_key, value in kwargs_dict.items():
                op_args[self.snake_to_camel(snake_key)] = value

            op_obj = client.service.__getitem__(operation)
            result = op_obj(session=session, **op_args)
            result_dict = zeep.helpers.serialize_object(result)

        return (True, result_dict)
