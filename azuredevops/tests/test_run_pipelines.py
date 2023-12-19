import requests_mock
from runPipeline import runPipeline
from st2tests.base import BaseActionTestCase


class RunPipelineTest(BaseActionTestCase):
    action_cls = runPipeline
    global pipelineId
    pipelineId = 12345678
    global project
    project = "195587f7-70bf-9cbe-9b80-9385875cd841"
    global org
    org = "testorg"
    global accesstoken
    accesstoken = "kjsahjkbfdnjkshhdkjhfkjhnskdjhfiuwheiufwgiugf2938g9f"
    global base_url
    base_url = f"https://dev.azure.com/{org}/{project}/_apis/"

    def test_run_pipeline(self):
        with requests_mock.Mocker() as m:
            m.post(
                f"{base_url}pipelines/12345678/runs?api-version=7.0",
                text=self.get_fixture_content("run_pipeline.json"),
            )

            m.get(
                f"{base_url}pipelines/12345678/runs/5377370",
                text=self.get_fixture_content("run_pipeline_done.json"),
            )

            result = self.get_action_instance().run(
                org=org,
                project=project,
                accesstoken=accesstoken,
                pipelineId=12345678,
                templateParameters="",
                refName="",
            )
            print(result)
            self.assertEqual(result, True)

    def test_run_pipeline_failed(self):
        with requests_mock.Mocker() as m:
            m.post(
                f"{base_url}pipelines/12345678/runs?api-version=7.0",
                text=self.get_fixture_content("run_pipeline.json"),
            )

            m.get(
                f"{base_url}pipelines/12345678/runs/5377370",
                text=self.get_fixture_content("run_pipeline_failed.json"),
            )

            with self.assertRaises(ValueError):
                self.get_action_instance().run(
                    org=org,
                    project=project,
                    accesstoken=accesstoken,
                    pipelineId=12345678,
                    templateParameters="",
                    refName="",
                )
