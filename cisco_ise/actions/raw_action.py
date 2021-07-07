from lib.base import BaseAction
from requests.auth import HTTPBasicAuth


class RawAction(BaseAction):

    def run(self, **kwargs):
        """ Run a raw action.
            This is intended for advanced usage and to enable future proofing
        """

        # Create a connection dict, if a connection_name was supplied, attempt to retrieve it
        connection = {}

        connection_name = kwargs.pop('connection_name', None)
        if connection_name:
            connection = self.retrieve_config_connection(connection_name)

        # Check if any connection fields were provided by the action
        # If found, override value in connection
        if 'api_user' in kwargs and kwargs['api_user']:
            connection['api_user'] = kwargs.pop('api_user', None)

        if 'api_pass' in kwargs and kwargs['api_pass']:
            connection['api_pass'] = kwargs.pop('api_pass', None)

        if 'verify_ssl' in kwargs and kwargs['verify_ssl']:
            connection['verify_ssl'] = kwargs.pop('verify_ssl', True)

        if 'verify_ssl' not in connection:
            connection['verify_ssl'] = True

        # Validate required Info
        if not connection['api_user']:
            raise ValueError(
                'Required Parameter api_user is missing')
        if not connection['api_pass']:
            raise ValueError(
                'Required Parameter api_pass is missing')

        payload = kwargs.pop('payload', None)

        auth = HTTPBasicAuth(connection['api_user'], connection['api_pass'])

        response_format = kwargs.pop('response_format', 'json')
        payload_format = kwargs.pop('payload_format', 'json')

        headers = {
            'Accept': f'application/{response_format}',
            'Content-Type': f'application/{payload_format}'
        }

        response_data, response_code, succeeded, response_msg = \
            self.api_request(http_method=kwargs['http_method'],
                             request_uri=kwargs['request_uri'],
                             auth=auth,
                             verify_ssl=connection['verify_ssl'],
                             data=payload,
                             headers=headers)

        return self.format_action_result(response_data,
                                         response_code,
                                         succeeded,
                                         response_msg)
