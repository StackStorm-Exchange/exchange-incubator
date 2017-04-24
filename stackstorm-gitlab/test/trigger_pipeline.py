#!/usr/bin/env python

from lib.gitlab import GitlabPipelineAPI


class GitlabPipelineTrigger(GitlabPipelineAPI):

    def run(self, url, project_id, ref, trigger_token, variables, token, verify_ssl):
        self.url = url or self.url
        self.verify_ssl = verify_ssl or self.verify_ssl
        self.token = token or self.token

        return True, self.post(self.url, project_id, ref, trigger_token, variables)


default_config = {
    "url": "http://git.mgmt",
    "token": "jTxgef-5ToTf8XR5HRkB",
    "verify_ssl": False,
}


test_config = {
    "url": "http://git.mgmt",
    "token": "jTxgef-5ToTf8XR5HRkB",
    "verify_ssl": False,
    "project_id": "32",
    "ref": "master",
    "trigger_token": "343560b0991211f4c6f1c5cd6b7077a",
    "variables": {
        "DEMO": True,
    }
}

c = GitlabPipelineTrigger(config=default_config)

print c.run(**test_config)

