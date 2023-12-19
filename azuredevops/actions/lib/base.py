from st2common.runners.base_action import Action


class BaseActionAdo(Action):
    def run(self, **kwargs):
        pass

    def __init__(self, config):
        super(BaseActionAdo, self).__init__(config=config)
        self.org_config = self.config.get("org", None)
        self.project_config = self.config.get("project", None)
        self.accesstoken_config = self.config.get("accesstoken", None)
