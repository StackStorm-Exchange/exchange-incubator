from run_operation import RunOperation


class RunLogout(RunOperation):

    def __init__(self, config):
        super(RunLogout, self).__init__(config)

    def _exec(self, context, client):
        # don't validate connection info for logout because
        # most of the connection parameters are not needed
        return client.service.Logout(session=context['session'])
