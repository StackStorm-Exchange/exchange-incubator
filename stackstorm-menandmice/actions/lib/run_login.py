from run_operation import RunOperation


class RunLogin(RunOperation):

    def __init__(self, config):
        super(RunLogin, self).__init__(config)

    def _exec(self, context, client):
        self.validate_connection(context['connection'])
        session = self.login(client, context['connection'])
        return {'session': session}
