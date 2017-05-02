#!/usr/bin/env python

from lib.gitlab import GitlabProjectsAPI


class GitlabProject(GitlabProjectsAPI):

    def run(self, url, project, token, verify_ssl):
        self.url = url or self.url
        self.verify_ssl = verify_ssl or self.verify_ssl
        self.token = token or self.token

        return True, self.get(self.url, project)


default_config = {
    "url": "http://git.mgmt",
    "token": "-ryDDqAyys77xeJH98UP",
    "verify_ssl": False,
}


test_config = {
    "url": "http://git.mgmt",
    "token": "cKzH-_1ygs1UHsAsMKXu",
    "project": "packs/foreman",
    "verify_ssl": False,
}

c = GitlabProject(config=default_config)

print c.run(**test_config)
