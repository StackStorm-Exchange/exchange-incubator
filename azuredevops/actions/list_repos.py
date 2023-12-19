import base64

import requests
from lib.base import BaseActionAdo


# -------------------------------------------------------------------------
# Define colors for output
# -------------------------------------------------------------------------
class runPipeline(BaseActionAdo):
    def run(self, org, project, accesstoken):
        if org == "none":
            org = self.org_config
        if project == "none":
            project = self.project_config
        if accesstoken == "none":
            accesstoken = self.accesstoken_config
        pat = str(base64.b64encode(bytes(":" + accesstoken, "ascii")), "ascii")
        authorization = "Basic " + pat
        ado_header = {
            "Authorization": authorization,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        ado_base_url = f"https://dev.azure.com/{org}/{project}/_apis"
        # -------------------------------------------------------------------------
        # Get the metadata for all repos from the Azure DevOps
        # repository in json format
        # -------------------------------------------------------------------------
        get_repo_url = (
            f"{ado_base_url}/git/repositories?api-version=7.1-preview.1"
        )
        response = requests.get(get_repo_url, headers=ado_header)
        # -------------------------------------------------------------------------
        # Initialize a dictionary to store the results
        # -------------------------------------------------------------------------
        if response.status_code == 200:
            return True, response.json()
        else:
            print(response.text)
            exit(1)
