from lib import action


class RunCmdlet(action.BaseAction):

    def run(self, **kwargs):
        cmdlet = kwargs['cmdlet']
        del kwargs['cmdlet']
        return self.run_hyperv_cmdlet(cmdlet, **kwargs)
