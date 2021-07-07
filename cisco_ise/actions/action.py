from lib.base import BaseAction


class Action(BaseAction):

    def run(self, **kwargs):
        """ Run action
        """

        # Check if action uses 'name' field instead of 'resource_id'
        # If it does, rebuild resource_id. Used to reduce input parameter confusion
        # Should come before other modifications incase there is no resource_id.
        name = kwargs.pop('name', None)
        if name:
            self.logger.debug('resource_id being populated from name parameter')
            kwargs['resource_id'] = f'/name/{name}'

        # Some API Endpoints have a trailing string after the ID.
        # If a parameter for this string is present, update the resource_id field.
        url_tail = kwargs.get('url_tail', None)
        if url_tail:
            self.logger.debug('adding /{url_tail} to resource_id')
            kwargs['resource_id'] = f"{kwargs['resource_id']}/{url_tail}"

        # Some API Endpoints have to specify a portal ID after the resource ID.
        # If a parameter for portal_id, update the resource_id field.
        portal_id = kwargs.get('portal_id', None)
        if portal_id:
            self.logger.debug('adding /portalId/{portal_id} to resource_id')
            kwargs['resource_id'] = f"{kwargs['resource_id']}/portalId/{portal_id}"

        # Call multiple methods that parse and prepare data
        # and creates objects that can be used to call api_request()
        self.action_setup(**kwargs)

        return self.api_client(
            http_method=self.http_method,
            request_uri=self.request_uri,
            api_user=self.connection['api_user'],
            api_pass=self.connection['api_pass'],
            verify_ssl=self.connection['verify_ssl'],
            payload=self.payload)
