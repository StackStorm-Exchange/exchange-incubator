#!/usr/bin/env python

from lib.gitlab import GitlabPipelineAPI


class GitlabPipelineTrigger(GitlabPipelineAPI):

    def run(self, url, project_id, ref, trigger_token, variables, token, verify_ssl):
        self.url = url or self.url
        self.verify_ssl = verify_ssl or self.verify_ssl
        self.token = token or self.token

        return True, dict(self.post(self.url, project_id, ref, trigger_token, variables))
