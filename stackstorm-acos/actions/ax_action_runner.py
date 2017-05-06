import acos_client as acos

from acoslib.action import BaseAction


class AXActionRunner(BaseAction):
    def run(self, api_version, action, object_path, **kwargs):
        client = self.login(api_version)
        if client:
            try:
                # transforms user parameters as needed
                kwargs = self._transform_params(client, object_path, action, **kwargs)

                _target_obj = self.get_object(client, object_path)

                return (True, getattr(_target_obj, action)(**kwargs))
            except acos.errors.AuthenticationFailure:
                return (False, 'An authentication error is occurr')
            except acos.errors.NotFound as e:
                return (False, e)
            except AttributeError:
                return (False, 'The acos_client has no interfaces for %s' % (object_path))
        else:
            return (False, 'Failed to initilaize Client object of acos_client')

    def _transform_params(self, client, object_path, action, **kwargs):
        if object_path == 'slb.service_group.member' and action == 'create':
            # transforms status parameter from boolean to the internal constant of acos-client
            if kwargs['status']:
                kwargs['status'] = client.slb.UP
            else:
                kwargs['status'] = client.slb.DOWN

        return kwargs
