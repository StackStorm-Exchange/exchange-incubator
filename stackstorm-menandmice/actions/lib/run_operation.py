from st2actions.runners.pythonrunner import Action

import zeep
import zeep.helpers

#                         (key, required, default)
CONFIG_CONNECTION_KEYS = [('server', True, ""),
                          ('username', True, ""),
                          ('password', True, ""),
                          ('port', False, ""),
                          ('transport', False, "http"),
                          ('wsdl_endpoint', False, "_mmwebext/mmwebext.dll?wsdl")]


class RunOperation(Action):

    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(RunOperation, self).__init__(config)

    def snake_to_camel(self, snake_cased_str):
        """Converts a snake_case_string into a camelCasedString
        :param snake_cased_str: snake cased string
        :returns: string converted into camel case
        """
        return self._convert_to_camel(snake_cased_str, "_")

    def _convert_to_camel(self, snake_cased_str, separator):
        components = snake_cased_str.split(separator)
        preffix = ""
        suffix = ""
        if components[0] == "":
            components = components[1:]
            preffix = separator
        if components[-1] == "":
            components = components[:-1]
            suffix = separator
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
        """Attempts to resolve the connection information by looking up information
        from action input parameters (highest priority) or from the config (fallback).
        :param kwargs_dict: dictionary of kwargs containing the action's input
        parameters
        :returns: a dictionary with the connection parameters (see: CONFIG_CONNECTION_KEYS)
        resolved.
        """
        connection_name = self.get_del_arg('connection', kwargs_dict)
        config_connection = None
        if connection_name:
            config_connection = self.config['menandmice'].get(connection_name)
            if not config_connection:
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
        """Ensures that all required parameters are in the connection. If a
        required parameter is missing a KeyError exception is raised.
        :param connection: connection to validate
        :returns: True if the connection is valid
        """
        for key, required, default in CONFIG_CONNECTION_KEYS:
            # ensure the key is present in the connection?
            if key in connection and connection[key]:
                continue

            # skip if this key is not required
            if not required:
                continue

            if connection['connection']:
                raise KeyError("config.yaml mising: menandmice:{0}:{1}"
                               .format(connection['connection'], key))
            else:
                raise KeyError("Because the 'connection' action parameter was"
                               " not specified, the following action parameter"
                               " is required: {0}".format(key))
        return True

    def build_wsdl_url(self, connection):
        """Creates a SOAP WSDL URL for Men&Mice with the following format:
        <transport>://<server>:<port>/<wsdl_endpoint>?server=localhost
        :param connection: connection dictionary with keys for all paremters
        needed to build the wsdl. This must be a valid connection.
        :returns: a string containing the WSDL URL for the connection.
        """
        if 'server' not in connection or not connection['server']:
            raise RuntimeError(("'server' is not specified in the config or given"
                                " as a parameter to the action. It must be provided"
                                " in one of these places in order to build the"
                                " wsdl URL!"))

        # example(s):
        #   http://menandmice.domain.tld/_mmwebext/mmwebext.dll?wsdl?server=localhost
        #   https://menandmice.domain.tld/_mmwebext/mmwebext.dll?wsdl?server=localhost
        #   http://menandmice.domain.tld:8080/_mmwebext/mmwebext.dll?wsdl?server=localhost
        #   https://menandmice.domain.tld:8443/_mmwebext/mmwebext.dll?wsdl?server=localhost
        wsdl_url = None
        if 'port' in connection and connection['port']:
            url_str = "{0}://{1}:{2}/{3}?server=localhost"
            wsdl_url = url_str.format(connection['transport'],
                                      connection['server'],
                                      connection['port'],
                                      connection['wsdl_endpoint'])
        else:
            url_str = "{0}://{1}/{2}?server=localhost"
            wsdl_url = url_str.format(connection['transport'],
                                      connection['server'],
                                      connection['wsdl_endpoint'])

        return wsdl_url

    def login(self, client, connection):
        """Performs the Men&Mice Login operation using the connection information
        and the zeep client that is initialized with the WSDL from the server.
        :param client: zeep client initialized with the WSDL from the server
        :param connection: connection dictionary that has been validated
        :returns: a string containing the login session cookie. If a login
        failure occurs a zeep exception will be raised.
        """
        session = client.service.Login(server=connection['server'],
                                       loginName=connection['username'],
                                       password=connection['password'])
        return session

    def _pre_exec(self, **kwargs):
        """Performs all work needed in order for the operation to execute.
        This method is designed to be overriden by subclasses.
        It must return a tuple containing a context object and a zeep client.
        The context object should be a dictionary with the following key/values:
            'kwarg_dict': the action's input parameters represented as a dictionary
            'operation': string representing the Men&Mice SOAP operation to execute
            'session': an optional login session passed in as an action input parameter
            'connection': connection dictionary object
            'wsdl_url': URL to the WSDL for the connection
        :returns: a tuple containing a context object
        """
        kwargs_dict = dict(kwargs)
        operation = self.get_del_arg('operation', kwargs_dict)
        session = self.get_del_arg('session', kwargs_dict)
        connection = self.resolve_connection(kwargs_dict)
        wsdl_url = self.build_wsdl_url(connection)
        client = zeep.Client(wsdl=wsdl_url)
        context = {'kwargs_dict': kwargs_dict,
                   'operation': operation,
                   'session': session,
                   'connection': connection,
                   'wsdl_url': wsdl_url}
        return (context, client)

    def _exec(self, context, client):
        """Executes the operation defined in the context using the client.
        This method is designed to be overriden by subclasses.
        :param context: context of the format defined by _pre_exec()
        :param client: zeep client
        :returns: A result object from performing the operation. This can
        be any built-in python type (string, int, list, dict) or a zeep
        object returned from executing the operation via zeep.
        """
        if not context['session']:
            self.validate_connection(context['connection'])
            context['session'] = self.login(client, context['connection'])

        op_args = {}
        for snake_key, value in context['kwargs_dict'].items():
            op_args[self.snake_to_camel(snake_key)] = value

        op_obj = client.service.__getitem__(context['operation'])
        result = op_obj(session=context['session'], **op_args)
        return result

    def _post_exec(self, result):
        """Converts the result object into a format that's acceptable to
        StackStorm. The results returned by zeep are custom object types
        that are not compatible with StackStorm. In order to return
        meaningful data from our operations we must convert them to
        python built-in datatypes (strings, ints, lists, dicts).
        :param result: the potentially incompatible result object
        :returns: a StackStorm compatible result object
        """
        result_dict = zeep.helpers.serialize_object(result, target_cls=dict)
        return result_dict

    def run(self, **kwargs):
        """Main entry point for the StackStorm actions to execute the operation.
        :returns: the result of the operation
        """
        context, client = self._pre_exec(**kwargs)
        result = self._exec(context, client)
        return self._post_exec(result)
