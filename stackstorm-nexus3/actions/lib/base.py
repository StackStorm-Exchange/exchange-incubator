import sys
from exception import *
from nexuscli.repository import Repository
from nexuscli.nexus_client import NexusClient
from nexuscli.exception import *

from st2common.runners.base_action import Action

__all__ = [
    'BaseAction'
]

REQUIRED_FIELDS = ['url', 'user', 'password']


class BaseAction(Action):

    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.nexus_profiles = self.config.get('profiles', {})
        self.nexus_client = None
        self.dial_config = None

    def validate_config(self, c_profile):
        """ Validate connection configuration

        """
        validation_errors = []
        is_valid = True
        for field in REQUIRED_FIELDS:
            if c_profile.get(field, None) == None:
                validation_errors.push("%s if missing" % field)
                is_valid = False

        return (is_valid, validation_errors)

    def get_connection_defaults(self):
        """ default properties

        """
        return {
            "url": self.config.get('url', None),
            "verify": self.config.get('verify', True),
            "user": self.config.get('user', None),
            "password": self.config.get('password', None)
        }

    def init_config(self, profile=None):
        """ Get nexus3 server connection string

        """
        self.dial_config = self.get_connection_defaults()
        if profile is not None:
            profile = profile.strip()
            if len(profile) == 0:
                profile = None

        # use 'default_profile' if 'config_profile' is empty
        if profile is None:
            profile = self.config.get('default_profile', None)

        # Use defaults options, if neither config_profile nor default_profile is provided
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
            self.nexus_client = NexusClient(**self.dial_config)
        except Exception as error:
            self.logger.error("Couldn't instantiate nexus client %s" % error)

    def get_resource_dialer(self, resource):
        """ return nexus_client

        """
        if self.nexus_client is None:
            raise NexusClientNotInstantiatedError(
                "Instantiate nexus_client by calling init_dialer() method first")
        return getattr(self.nexus_client, resource)

    def intent_list(self, resource, **kwargs):
        """ Intent: List

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
            response = "Failed to create %s. Most likely reason, same name resource already exist." % (
                resource)
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
            response = "Invalid resource: %s(supported only scripts)" % resource

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
