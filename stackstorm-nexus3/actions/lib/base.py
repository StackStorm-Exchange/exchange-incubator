from st2common.runners.base_action import Action
from exception import MissingProfileError
from exception import ValidationFailError
from exception import NexusClientNotInstantiatedError
from nexuscli.repository import Repository
from nexuscli.nexus_client import NexusClient
from nexuscli.exception import NexusClientAPIError
from nexuscli.exception import NexusClientCreateRepositoryError


__all__ = [
    'BaseAction'
]

REQUIRED_FIELDS = ['url', 'user', 'password']


class BaseAction(Action):

    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.nexus_profiles = self.config.get('profiles', {})
        self._client = None
        self.dial_config = None

    def validate_config(self, c_profile):
        """ Validate connection configuration
        This function returns a tuple of (is_valid, errors), where errors is
        a list of all of the missing fields in a profile. This is avoid
        making users having to correct each missing field at a time.
        """
        validation_errors = []
        is_valid = True
        for field in REQUIRED_FIELDS:
            if c_profile.get(field) is None:
                validation_errors.append(
                    "Required parameter %s is missing" % field)
                is_valid = False

        return (is_valid, validation_errors)

    def get_connection_defaults(self):
        """ Default properties

        """
        return {
            "url": self.config.get('url', None),
            "verify": self.config.get('verify', True),
            "user": self.config.get('user', None),
            "password": self.config.get('password', None)
        }

    def init_config(self, profile=None):
        """ Generate connection config and validate it

        """
        self.dial_config = self.get_connection_defaults()
        profile = profile if profile and len(profile.strip()) > 0 else None

        # use 'default_profile' if 'config_profile' is empty
        if profile is None:
            profile = self.config.get('default_profile', None)

        # Use defaults options, if neither config_profile nor default_profile
        #  is provided
        if profile is None:
            self.logger.info("using defaults connection values")
        else:
            c_profile = self.nexus_profiles.get(profile, None)
            if c_profile is None:
                raise MissingProfileError(
                    "connection profile not found: '%s'" % profile)

            self.dial_config.update(c_profile)

        # Validate configuration
        (is_valid, errors) = self.validate_config(self.dial_config)
        if not is_valid:
            raise ValidationFailError(
                "Validation failed: %s" % errors)

        return self.dial_config

    def init_dialer(self):
        try:
            self.logger.debug("connection string: %s \n" % self.dial_config)
            self._client = NexusClient(**self.dial_config)
        except Exception as error:
            self.logger.error("Couldn't instantiate nexus client %s" % error)
            raise error

    def get_resource_dialer(self, resource):
        """ return nexus client

        """
        if self._client is None:
            raise NexusClientNotInstantiatedError(
                "Instantiate nexus_client by calling \
                    init_dialer() method first")
        return getattr(self._client, resource)

    def intent_list(self, resource, **kwargs):
        """ Intent: LIST

        """
        dialer = self.get_resource_dialer(resource)
        is_success = True
        response = {}
        if resource == "repositories":
            response = dialer.raw_list()
        else:
            response = dialer.list()

        return (is_success, response)

    def intent_get(self, resource, **kwargs):
        """ Intent: GET

        """
        dialer = self.get_resource_dialer(resource)
        is_success = True
        response = {}
        if resource == "repositories":
            response = dialer.get_raw_by_name(kwargs.pop('name'))
        else:
            response = dialer.get(kwargs.pop('name'))

        return (is_success, response)

    def intent_create(self, resource, **kwargs):
        """ Intent: CREATE

        """
        dialer = self.get_resource_dialer(resource)
        is_success = True
        response = {}
        payload = kwargs.get('data', '')

        if resource == "repositories":
            repo_type = kwargs.pop('type')
            payload = Repository(repo_type, **kwargs)

        try:
            if resource == "scripts":
                response = dialer.create_if_missing(payload)
            else:
                response = dialer.create(payload)
        except NexusClientCreateRepositoryError as error:
            response = "Failed to create %s. Reason: %s" % (resource, error)
            is_success = False

        return (is_success, response)

    def intent_run(self, resource, **kwargs):
        """ Intent: RUN

        """
        dialer = self.get_resource_dialer(resource)
        is_success = True
        response = {}
        if resource == "scripts":
            response = dialer.run(kwargs.pop('name'), kwargs.pop('data'))
        else:
            is_success = False
            response = "Invalid resource: %s\
                (supported only scripts)" % resource

        return (is_success, response)

    def intent_delete(self, resource, **kwargs):
        """ Intent: DELETE

        """
        dialer = self.get_resource_dialer(resource)
        is_success = True
        response = {}
        try:
            response = dialer.delete(kwargs.pop('name'))
        except NexusClientAPIError as error:
            is_success = False
            response = error

        return (is_success, response)
