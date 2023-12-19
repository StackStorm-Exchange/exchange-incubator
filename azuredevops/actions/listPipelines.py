import base64

import requests
from lib.base import BaseActionAdo


class listPipeline(BaseActionAdo):
    def run(self, org, project, accesstoken):
        if org == "none":
            org = self.org_config
        if project == "none":
            project = self.project_config
        if accesstoken == "none":
            accesstoken = self.accesstoken_config
        authorization = str(
            base64.b64encode(bytes(":" + accesstoken, "ascii")), "ascii"
        )
        url = (
            "https://dev.azure.com/"
            + org
            + "/"
            + project
            + "/_apis/pipelines?api-version=7.0"
        )
        accesstoken = "Basic " + authorization
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": accesstoken,
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return True, response.json()
        else:
            print(response.text)
            exit(1)
