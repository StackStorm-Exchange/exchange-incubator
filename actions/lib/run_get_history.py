from lib.run_operation import RunOperation


class RunGetHistory(RunOperation):

    def __init__(self, config):
        super(RunGetHistory, self).__init__(config)

    def _pre_exec(self, **kwargs):
        context, client = super(RunGetHistory, self)._pre_exec(**kwargs)

        # username parameter was renamed in generate because
        # it conflicted with the username from the connection
        # undo that rename here so it's passed properly
        if context['operation'] == 'GetHistory':
            context['kwargs_dict']['username'] = context['kwargs_dict']['user_name']
            del context['kwargs_dict']['user_name']

        return (context, client)
