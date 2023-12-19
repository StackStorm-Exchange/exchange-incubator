import base64
import socket

import requests
from lib.base import BaseActionAdo


class ConvertUserStorys(BaseActionAdo):
    def run(self, org, project, ado_accesstoken, ado_team):
        if org == "none":
            org = self.org_config
        if project == "none":
            project = self.project_config
        if ado_accesstoken == "none":
            ado_accesstoken = self.accesstoken_config
        ADO_API_ROOT = f"https://dev.azure.com/{org}/{project}/"

        # -------------------------------------------------------------------------
        # This Function:
        # 1) Query all New UserStorys from a Project.
        # 2) Check if User Storys have already a linked Workitem
        # 3) Create a new Task as copy from the User Story
        # 4) Link the User Story to the WorkItem.
        # -------------------------------------------------------------------------
        def convert_userstory(ado_accesstoken):
            authorization = str(
                base64.b64encode(bytes(":" + ado_accesstoken, "ascii")),
                "ascii",
            )
            accesstoken = "Basic " + authorization
            url = ADO_API_ROOT + ado_team + "/_apis/wit/wiql?api-version=6.0"
            payload = {
                "query": (
                    "Select [System.Id], [System.Title], "
                    "[System.State] From WorkItems "
                    "WHERE [System.State] IN ('New')"
                    " AND [System.WorkItemType] = 'User Story'"
                    " AND [System.TeamProject] = @Project"
                )
            }

            try:
                r = requests.post(
                    url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": accesstoken,
                    },
                )
            except ConnectionRefusedError as cre:
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                print(
                    f"'{hostname}' [{ip_address}] is unable to reach'"
                    f"' 'https://dev.azure.com {cre}'"
                )
                return
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                return

            if r.status_code == requests.codes.ok:
                pass
            else:
                print(
                    f"Request unsuccessful => {r.status_code}"
                    f" {r.content} - exiting"
                )

            json = r.json()
            workitems_list = []
            print(json["workItems"])
            for work in json["workItems"]:
                url = work["url"] + "?%24expand=1"
                try:
                    r = requests.get(
                        url,
                        headers={
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "Authorization": accesstoken,
                        },
                    )
                except ConnectionRefusedError as cre:
                    hostname = socket.gethostname()
                    ip_address = socket.gethostbyname(hostname)
                    print(
                        f"'{hostname}' [{ip_address}] is'"
                        f"' unable to reach 'https://dev.azure.com {cre}'"
                    )
                    return
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
                    return
                if r.status_code == requests.codes.ok:
                    pass
                else:
                    print(
                        f"Request unsuccessful =>"
                        f" {r.status_code} {r.content} - exiting"
                    )
                object = r.json()
                object = object["fields"]
                relations = r.json()
                # Check if there is already a Relation
                if "relations" in relations:
                    relations = relations["relations"]
                    print(
                        f"Relation Key exist for: "
                        f"{object['System.Title']}"
                        f" that are the Relations {relations}"
                    )
                else:
                    print(f"No Relations exist. for {object['System.Title']}")
                    workitems_list.append(object["System.Title"])
                    print("Create Task")
                    url = (
                        ADO_API_ROOT
                        + "_apis/wit/workitems/$Task?api-version=6.0"
                    )
                    data = [
                        {
                            "op": "add",
                            "path": "/fields/System.Title",
                            "value": str(object["System.Title"]),
                        },
                        {
                            "op": "add",
                            "path": "/fields/System.WorkItemType",
                            "value": "Task",
                        },
                        {
                            "op": "add",
                            "path": "/fields/System.Description",
                            "value": str(object["System.Description"]),
                        },
                        {
                            "op": "add",
                            "path": "/relations/-",
                            "value": {
                                "rel": "System.LinkTypes.Hierarchy-Reverse",
                                "url": work["url"],
                                "attributes": {
                                    "comment": "Link to Parent User Story"
                                },
                            },
                        },
                    ]
                    try:
                        r = requests.post(
                            url,
                            json=data,
                            headers={
                                "Content-Type": "application/json-patch+json",
                                "Accept": "application/json",
                                "Authorization": accesstoken,
                            },
                        )
                    except ConnectionRefusedError as cre:
                        hostname = socket.gethostname()
                        ip_address = socket.gethostbyname(hostname)
                        print(
                            f"'{hostname}' [{ip_address}] is unable'"
                            f"' to reach 'https://dev.azure.com {cre}'"
                        )
                        return
                    except requests.exceptions.RequestException as e:
                        print(f"Error: {e}")
                        return
                    if r.status_code == requests.codes.ok:
                        print(r.text)
                    else:
                        print(
                            f"Request unsuccessful =>"
                            f" {r.status_code} {r.content} - exiting"
                        )
            return workitems_list

        print(convert_userstory(ado_accesstoken))
