#!/usr/bin/env python

from lib.gitlab import GitlabPipelineAPI


class GitlabPipeline(GitlabPipelineAPI):

    def run(self, url, project, token, verify_ssl):
        self.url = url or self.url
        self.verify_ssl = verify_ssl or self.verify_ssl
        self.token = token or self.token

        return True, self.get(self.url, project, self.token)


default_config = {
    "url": "http://git.mgmt",
    "token": "-ryDDqAyys77xeJH98UP",
    "verify_ssl": False,
}


test_config = {
    "url": "http://git.mgmt",
    "token": "-ryDDqAyys77xeJH98UP",
    "project": "packs/foreman",
    "verify_ssl": False,
}

c = GitlabPipeline(config=default_config)

__, k = c.run(**test_config)
for p in k:
    print p
