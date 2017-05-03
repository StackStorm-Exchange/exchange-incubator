#!/usr/bin/env python

from lib.gitlab import GitlabPipelineAPI


class GitlabPipeline(GitlabPipelineAPI):

    def run(self, url, project, token, verify_ssl):
        self.url = url or self.url
        self.verify_ssl = verify_ssl or self.verify_ssl
        self.token = token or self.token

        return True, self.get(self.url, project, self.token)
