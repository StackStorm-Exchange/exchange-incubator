from st2common.runners.base_action import Action
from requests.auth import HTTPBasicAuth

import sys
import requests
import json

# Constants
HTTPS_PORT = 9060
HTTP_PORT = 80

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE"]

#                   key, required, default
CONNECTION_FIELDS = [
    ("api_user", True, None),
    ("api_pass", True, None),
    ("hostname", True, None),
    ("verify_ssl", True, True),
    ("use_http", True, False),
]

MAX_PAGE_SIZE = 100

#                           http_code, message
HTTP_STATUS_RESPONSE_MESSAGE = [
    (201, "Resource was successfully created"),
    (204, "Resource was successfully deleted"),
]


class BaseAction(Action):
    """The base class for all actions"""

    def __init__(self, config):
        """init method, run at class creation"""
        super(BaseAction, self).__init__(config)
        self.logger.debug("Instantiating BaseAction()")

        # These will be populated with values once setup methods are ran
        self.action_kwargs = None
        self.base_api_resource = None
        self.connection = None
        self.connection_name = None
        self.filter_list = None
        self.filter_type = None
        self.http_method = None
        self.payload = None
        self.payload_format = None
        self.request_uri = None
        self.resource_id = None
        self.response_format = None
        self.sort_field = None
        self.sort_order = None

    def action_setup(self, **kwargs):
        """The base method that performs all the required data preperations.
        Not required if the action handles its own parsing of params to get URI/Data
        """

        # Basic housekeeping for running the action.
        # Creates self.action_kwargs and others
        self._prepare_kwargs(**kwargs)

        # Setup the connection details and parse Config Vs Action parameters.
        # Creates self.connection
        self._setup_connection(CONNECTION_FIELDS)

        # Perpare the URL string to use with the request.
        # Creates to self.request_uri
        self._prepare_uri()

        # Return True incase something cares to check
        return True

    def api_client(
        self,
        http_method=None,
        request_uri=None,
        api_user=None,
        api_pass=None,
        verify_ssl=True,
        payload=None,
        payload_format=None,
    ):

        """Parse data, prepare the request, and call the api_request()
        This API Client holds your hand through request process.
        If you just want to send things directly, use api_request()
        """

        # Check that the HTTP method we are attempting to use is in the
        # list of valid methods (HTTP_METHODS)
        if http_method not in HTTP_METHODS:
            raise KeyError(
                'http_method is a required parameter for "requests" and must be one of '
                f'"{HTTP_METHODS}". Method Supplied: {http_method}'
            )

        if not request_uri:
            self.logger.error("api_request(request_uri) is required, but none provided")
            sys.exit(1)

        # Check if formatting details were passed
        # if not, check if self.payload_format exists and use that value
        # If it doesn't exist, just set it to JSON
        if not payload_format:
            payload_format = "json" if self.payload_format is None else self.payload_format

        # Validate payload_format
        if payload_format not in ["json", "xml"]:
            self.logger.error(
                f'Valid types for payload_format are ["json", "xml"]. Received "{payload_format}"'
            )
            sys.exit(1)

        headers = {
            "Accept": "application/json",
            "Content-Type": f"application/{payload_format}",
        }

        auth = HTTPBasicAuth(api_user, api_pass)

        # GET and DELETE don't need a payload sent
        # Sometimes a GET will be a 'Get-All' which is effectively a search.
        # In that case, results need to be handled variably
        if http_method in ["GET", "DELETE"]:
            result = []
            last = False

            # Run the api_request() on a loop until we have no more pages
            # page['SearchResult']['nextPage']
            while not last:
                page, response_code, succeeded, response_msg = self.api_request(
                    http_method,
                    request_uri,
                    auth=auth,
                    headers=headers,
                    verify_ssl=verify_ssl,
                )

                # Check if there is a 'SearchResult'
                # 'SearchResult' is present on a 'Get-All' kind of request
                # and will contain a list of results and potentially a 'nextPage'
                if "SearchResult" in page:
                    # Check if there is a 'nextPage'
                    if "nextPage" in page["SearchResult"]:
                        request_uri = page["SearchResult"]["nextPage"]["href"]
                    else:
                        last = True

                    # If there was 'SearchResult', 'resources' should have the data we care about
                    if "resources" in page["SearchResult"]:
                        result.extend(page["SearchResult"]["resources"])

                # Looks like this isn't a 'Get-All' so there is probably just 1 key in page
                else:
                    result = page
                    last = True

            # All pages have been processed, return the applicable result and break the loop
            return self.format_action_result(
                result, response_code, succeeded, response_msg
            )

        # Not a GET or DELETE, send payload data, and result should be a dictionary and no paging
        elif http_method in ["POST", "PUT"]:
            response_data, response_code, succeeded, response_msg = self.api_request(
                http_method,
                request_uri,
                auth=auth,
                headers=headers,
                verify_ssl=verify_ssl,
                data=payload,
            )

            return self.format_action_result(
                response_data, response_code, succeeded, response_msg
            )

    def api_request(
        self,
        http_method=None,
        request_uri=None,
        auth=None,
        verify_ssl=True,
        data=None,
        headers=None,
    ):
        """The raw API Request execution.
        Can be called directly if you know exactly what you want sent to the API
        Returns a tuple of (response_data, response_code, succeeded, response_msg)
        """

        # Check if passed data is a JSON serializable dict, otherwise treat it as a string.
        if type(data) is dict:
            data = json.dumps(data)
        else:
            data = str(data)

        try:
            client = requests.request(
                http_method,
                request_uri,
                auth=auth,
                headers=headers,
                verify=verify_ssl,
                data=data,
            )
        except Exception as err:
            self.logger.error(
                f'"api_request()" An error occured when executing the API Query. "{err}"'
            )
            sys.exit(1)

        response_data = {}

        # Check if the response data is parsable, if not just return an empty dict.
        try:
            client.json()
        except Exception:
            if getattr(client, "text", None):
                response_data = client.text
        else:
            response_data = client.json()

        response_code = client.status_code

        # Most results will return useful data to intepret results.
        # Creates and Deletes only return details when something goes wrong.
        # Look for quiet success codes, and grab a useful message to send from
        # HTTP_STATUS_RESPONSE_MESSAGE
        response_msg = ""
        for status, msg in HTTP_STATUS_RESPONSE_MESSAGE:
            if response_code == status:
                response_msg = msg
                break

        # Many fauilure conditions will result in the action succeeding.
        # This isn't a bad thing, but we need to have a simple check to know
        # If what we tried worked or not. Any non 2xx reponse means something didn't work
        # https://developer.cisco.com/docs/identity-services-engine/#!error-codes
        if client.ok:
            succeeded = True
        else:
            succeeded = False

        return (response_data, response_code, succeeded, response_msg)

    def retrieve_config_connection(self, connection_name=None):
        """Checks the pack config for a named connection entry
        and returns a dict with connection params from config entry.
        If no config found, returns an empty dict {}
        """

        try:
            config_connection = self.config["connections"].get(connection_name, None)
        except Exception as err:
            self.logger.error(f'Specified connection "{connection_name}" Error: {err}')
            sys.exit(1)
        # If we found a valid config (not None), set it as the connection
        if config_connection:
            self.logger.debug(
                f'Connection with name "{connection_name}" loaded from pack configuration'
            )
            return config_connection
        # didn't find the connection_name in the config
        else:
            self.logger.warning(
                f'Connection with name "{connection_name}" not found in configuration'
            )
            # return an empty dictionary
            return {}

    def format_action_result(
        self, response_data=None, response_code=None, succeeded=None, response_msg=None
    ):
        """Handles formatting to ensure consistent results formatting"""
        return {
            "data": response_data,
            "response_code": response_code,
            "succeeded": succeeded,
            "response_msg": response_msg,
        }

    def _setup_connection(self, connection_fields):
        """Handles the logic for determining what credentials/hostname to use.
        Resolves conflicts between config values, and action values

        Priority: Action Specified Value > Config Value
        """

        if self.action_kwargs is None:
            raise NameError(
                "_prepare_kwargs() is required to be ran prior to _setup_connection()"
            )

        # dict to either replace with a config connection, or load Action values into
        connection = {}

        if self.connection_name:
            connection = self.retrieve_config_connection(
                connection_name=self.connection_name
            )

        # Evaluate the connection fields provided for this specific API
        for key, required, default in connection_fields:
            # Prefer values found from the action Over the ones from the config
            if self.action_kwargs.get(key, None) not in [None, ""]:
                connection[key] = self.action_kwargs.pop(key)
                continue
            elif connection and key in connection:
                if connection[key] or connection[key] is False:
                    pass
            # If we haven't found the key yet, check if it's required
            elif required:
                # False is potentially a valid default value for a boolean
                if default or default is False:
                    connection[key] = default

                # No usable default or value passed, time to fail.
                else:
                    raise ValueError(
                        f'Required Parameter "{key}" missing with no suitable default.'
                    )

            # If the key is still in action_kwargs and its related to connection, remove it
            if key in self.action_kwargs:
                del self.action_kwargs[key]

        _u1 = connection["api_user"][:1]
        _u2 = connection["api_user"][-2:]
        self.logger.debug(f'Connection setup using User: "{_u1}***{_u2}"')

        self.connection = connection

        return True

    def _prepare_kwargs(self, **kwargs):
        """Takes care of all the setup and validation that needs to be done before trying
        the API Client method api_request()
        """

        # Extract well known parameters

        self.connection_name = kwargs.pop("connection_name", None)

        # HTTP Method used for request
        self.http_method = kwargs.pop("http_method", None)
        # Check that the HTTP method we are attempting to use is in the list of valid methods
        if self.http_method not in HTTP_METHODS:
            raise KeyError(
                f'http_method is a required parameter for "requests" and must be one of '
                f'"{HTTP_METHODS}". Method Supplied: {self.http_method}'
            )

        # The base resource used for this API Request
        # https://ise-pan.domain.com:9060/ers/config/{base_api_resource}
        self.base_api_resource = kwargs.pop("base_api_resource", None)
        # If the base_api_resource already has a preceeding '/', it should be removed.
        if self.base_api_resource.startswith("/"):
            self.base_api_resource = self.base_api_resource[1:]
        # Check that the HTTP method we are attempting to use is in the list of valid methods
        if not self.base_api_resource:
            raise ValueError(
                "base_api_resource is a required parameter to build the URI for the API Request. "
                f"base_api_resource recieved: {self.base_api_resource}"
            )

        # if present, the ID for the API resource
        self.resource_id = kwargs.pop("resource_id", None)
        # Does not require validation because not all actions will have this

        # if present, the Payload for the request (POST/PUT)
        self.payload = kwargs.pop("payload", None)
        # Does not require validation because not all actions will have this, and
        # JSON Schema is used on the action

        # https://developer.cisco.com/docs/identity-services-engine/#!searching-a-resource
        # extract the filter operator (AND OR)
        self.filter_type = kwargs.pop("filter_type", None)
        self.filter_list = kwargs.pop("filter_list", None)

        # https://developer.cisco.com/docs/identity-services-engine/#!searching-a-resource/sorting
        self.sort_order = kwargs.pop("sort_order", None)
        self.sort_field = kwargs.pop("sort_field", None)

        # ISE Supports Payloads and responses in either JSON or XML,
        # if not specified set both to json.
        # https://developer.cisco.com/docs/identity-services-engine/#!request-headers/request-headers
        self.response_format = kwargs.pop("response_format", "json")
        self.payload_format = kwargs.pop("payload_format", "json")

        # Assign kwargs to a class object so its easy to manipulate/reference later
        self.action_kwargs = kwargs

        return True

    def _prepare_uri(self):
        """Parses data into a URI String that can be used by the API client"""

        if self.connection is None:
            raise NameError(
                "_setup_connection() is required to be ran prior to _prepare_uri()"
            )

        # Check if protocol should be HTTP, if not set it to HTTPS
        if self.connection["use_http"]:
            protocol = "http"
        else:
            protocol = "https"

        # if we have a resource_id, we need to add it into the URI after the base_api_resource
        if self.resource_id:
            api_resource = f"{self.base_api_resource}/{self.resource_id}"
        else:
            api_resource = f"{self.base_api_resource}"

        # construct the base uri
        _h = self.connection["hostname"]
        if self.connection["use_http"]:
            self.request_uri = f"{protocol}://{_h}:{HTTP_PORT}/ers/config/{api_resource}"
        else:
            self.request_uri = f"{protocol}://{_h}:{HTTPS_PORT}/ers/config/{api_resource}"

        # Static Example:
        # https://ise-server.domain.com:9060/ers/config/internaluser

        # Sorting/Filtering Resources is only used with GET HTTP Method
        # https://developer.cisco.com/docs/identity-services-engine/#!searching-a-resource
        if self.http_method == "GET":
            search = self._prepare_search()

            # Update request_uri to include filtering and sort details
            self.request_uri = f"{self.request_uri}?size={MAX_PAGE_SIZE}{search}"
            # Static Example:
            # https://ise-server.domain.com:9060/ers/config/internaluser?size=100&sortasc=name&filtertype=and&filter=name.STARTW.a

        self.logger.debug(f"Request URI: {self.request_uri}")

        return True

    def _prepare_search(self):
        """When needed for GET HTTP requests, parses and prepares a single string
        that can be added into the URI
        """

        if self.action_kwargs is None:
            raise NameError(
                "_prepare_kwargs() is required to be ran prior to _setup_connection()"
            )

        # deafults to "name"
        if self.sort_field:
            sort_field = self.sort_field
        else:
            sort_field = "name"

        # defaults to 'ascending' order
        if self.sort_order and self.sort_order == "Descending":
            sort = f"&sortdsc={sort_field}"
        else:
            sort = f"&sortasc={sort_field}"

        # defaults to AND when not specified.
        if self.filter_type and self.filter_type == "OR":
            filter_type = "&filtertype=or"
        else:
            filter_type = "&filtertype=and"

        # Defaults to no filters
        if self.filter_list:
            filter_list_str = f"{filter_type}"
            for _filter in self.filter_list:
                filter_list_str = f"{filter_list_str}&filter={_filter}"

        else:
            filter_list_str = ""

        # Put it all together
        # sort will be something like "&sortasc=name"
        # filter_list_str will be something like "&filtertype=and&filter=name.STARTW.a" or ""
        return f"{sort}{filter_list_str}"
