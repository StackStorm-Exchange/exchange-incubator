import base64
import re
from datetime import datetime
from datetime import timedelta

import requests
from lib.base import BaseActionAdo


# -------------------------------------------------------------------------
# Define colors for output
# -------------------------------------------------------------------------
class runPipeline(BaseActionAdo):
    def run(self, org, project, repository, accesstoken, filter, retention):
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
        delete_date = (datetime.now() - timedelta(days=retention)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        # -------------------------------------------------------------------------
        # Get the metadata for all branches from the Azure DevOps
        # repository in json format
        # -------------------------------------------------------------------------
        get_branches_url = (
            f"{ado_base_url}/git/repositories/{repository}"
            "/refs?api-version=7.1-preview.1"
        )
        get_branches_response = requests.get(
            get_branches_url, headers=ado_header
        )

        if get_branches_response.status_code == 200:
            values = get_branches_response.json()["value"]
            # -------------------------------------------------------------------------
            # Store all branches in the variable ref_branches
            # but not the branches in the filter
            # -------------------------------------------------------------------------
            for all_branches in values:
                all_branches_names = all_branches["name"]
                ref_branches = []
                feature_branches = []
                if not re.search(filter, all_branches_names):
                    ref_branches.append(all_branches_names)
                # -------------------------------------------------------------------------
                # Cut off the string refs/heads/ from the branch names
                # and store the value in the variable feature_branches
                # -------------------------------------------------------------------------
                for x in ref_branches:
                    raw_feature_branches = x.replace("refs/heads/", "")
                    feature_branches.append(raw_feature_branches)
                # -------------------------------------------------------------------------
                # Check date of the last commit of each branch
                # -------------------------------------------------------------------------
                for affected_branches in feature_branches:
                    get_commit_url = (
                        f"{ado_base_url}/git/repositories/{repository}"
                        f"/commits?"
                        f"searchCriteria.$top=1&"
                        f"searchCriteria.itemVersion.version="
                        f"{affected_branches}&"
                        f"api-version=7.1-preview.1"
                    )
                    get_commit_response = requests.get(
                        get_commit_url, headers=ado_header
                    )
                    # -------------------------------------------------------------------------
                    # Check if branch needs to be deleted
                    # -------------------------------------------------------------------------
                    if get_commit_response.status_code == 200:
                        commit_date = get_commit_response.json()["value"]
                        for z in commit_date:
                            last_commit_date = z["committer"]["date"]
                            # -------------------------------------------------------------------------
                            # Branch gets deleted
                            # -------------------------------------------------------------------------
                            if last_commit_date < delete_date:
                                # -------------------------------------------------------------------------
                                # Function for removal
                                # -------------------------------------------------------------------------
                                removal_body = [
                                    {
                                        "name": all_branches["name"],
                                        "oldObjectId": all_branches[
                                            "objectId"
                                        ],
                                        "newObjectId": (
                                            "000000000000000000"
                                            "0000000000000000000000"
                                        ),
                                    }
                                ]
                                remove_branches_response = requests.post(
                                    get_branches_url,
                                    headers=ado_header,
                                    json=removal_body,
                                )
                                if remove_branches_response.status_code == 200:
                                    print(
                                        "Branch "
                                        + all_branches["name"]
                                        + " => REMOVED"
                                    )
                                else:
                                    print(
                                        "API Call to remove branch failed on "
                                        + get_branches_url
                                        + "Response: "
                                        + remove_branches_response
                                    )
                            # -------------------------------------------------------------------------
                            # Branch is newer and will remain
                            # -------------------------------------------------------------------------
                            elif last_commit_date > delete_date:
                                print(
                                    "Branch "
                                    + affected_branches
                                    + " => WILL REMAIN"
                                )
                            # -------------------------------------------------------------------------
                            # Branch is equal and will remain
                            # -------------------------------------------------------------------------
                            else:
                                print(
                                    "Branch "
                                    + affected_branches
                                    + " => WILL REMAIN"
                                )
                    else:
                        print(
                            "API Call to get commits failed on "
                            + get_commit_url
                            + " Response: "
                            + get_commit_response
                        )
                        exit(1)
        else:
            print(
                "API Call to get branches failed on "
                + get_branches_url
                + "Response: "
                + get_branches_response
            )
            exit(1)
