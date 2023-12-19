import base64
import json

import requests
from lib.base import BaseActionAdo


class runPipeline(BaseActionAdo):
    def run(
        self,
        org,
        project,
        accesstoken,
        pipelineId,
        templateParameters,
        refName,
    ):
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
            + str(org)
            + "/"
            + str(project)
            + "/_apis/pipelines/"
            + str(pipelineId)
            + "/runs?api-version=7.0"
        )
        print(f"url is: {url}")
        accesstoken = "Basic " + authorization
        payload = json.dumps(
            {
                "resources": {"repositories": {"self": {"refName": refName}}},
                "templateParameters": templateParameters,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": accesstoken,
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        pipeline_status = response.json()
        print(pipeline_status)
        pipeline_status = pipeline_status["url"]
        lopp_exit = False
        while lopp_exit is False:
            pipeline_status_response = requests.request(
                "GET", pipeline_status, headers=headers
            )
            pipeline_status_response = pipeline_status_response.json()
            pipeline_status_response = pipeline_status_response["state"]
            if pipeline_status_response != "inProgress":
                lopp_exit = True
        if pipeline_status_response == "completed":
            return True
        else:
            raise ValueError(
                f"Pipeline Failed with that Status: {pipeline_status_response}"
            )
