from st2tests.base import BaseActionTestCase
from st2client.commands import action as st2action
from with_items import WithItemsAction
import mock

def mock_sleep(time):
    pass

class ActionMockStatus(object):
    def __init__(self, id, status):
        self.status = status
        self.id = str(id)
        self.result = {"test":"OK"}


class LiveActions(object):
    def __init__(self, *args, **kwargs):
        self.execution_status = {}
        self.actions = {}
        self.action_id_counter = 0
        self.actions_seen = {}
    def query(self, id):
        """
        :param ids: list[str]
        """
        ids = [i for i in id.split(",")]
        results = []
        for id in ids:
            if self.actions_seen.get(id, False) == True:
                self.actions[id].status = st2action.LIVEACTION_STATUS_SUCCEEDED
                results.append(self.actions[id])
            if self.actions[id].status == st2action.LIVEACTION_STATUS_RUNNING:
                self.actions_seen[id] = True
                results.append(self.actions[id])
        return results
    def create(self, *args, **kwargs):
        action = ActionMockStatus(self.action_id_counter,
                st2action.LIVEACTION_STATUS_RUNNING)
        self.action_id_counter += 1
        self.actions[action.id] = action
        return action


class MockClient(object):
    def __init__(self, *args, **kwargs):
        self.mock_live_actions = LiveActions()
        self.liveactions = self.mock_live_actions

    @property
    def executions(self):
        return self.liveactions


class WithItemsTestCase(BaseActionTestCase):
    action_cls = WithItemsAction
    CONFIG = {
            "st2apiurl": "http://test/auth",
            "st2baseurl": "http://test/",
            "st2authurl": "http://test/auth"
            }

    def test_action_with_items_unescape_jinja(self):
        list_jinja = ["{_{xxx}_}"]
        dict_jinja = {"x":"{_{xxx}_}"}
        str_jinja = "{_{ xxx }_}"
        action = self.get_action_instance(config=WithItemsTestCase.CONFIG)
        res = action.unescape_jinja(list_jinja)
        self.assertEquals(["{{xxx}}"], res)
        res = action.unescape_jinja(dict_jinja)
        self.assertEquals({"x":"{{xxx}}"}, res)
        res = action.unescape_jinja(str_jinja)
        self.assertEquals("{{ xxx }}", res)

    def test_action_with_items_render_jinja(self):
        mock_result = {"test":1, "test2":2}
        result_context = {"_":{"result": mock_result}}
        action = self.get_action_instance(config=WithItemsTestCase.CONFIG)
        res = action.render_jinja(result_context,
                action.unescape_jinja_str("{_{ _.result.test2 }_}"))
        self.assertEquals(2, res)

    @mock.patch('with_items.Client')
    @mock.patch('with_items.time')
    def test_action_with_items_run(self, mock_time, mock_client):
        mock_time.sleep.side_effect = mock_sleep
        mock_client.side_effect = MockClient
        action = self.get_action_instance(config=WithItemsTestCase.CONFIG)
        list_params = [
                {"value1":True},
                {"value1":True},
                {"value1":True},
                {"value1":True},
                {"value1":True},
                {"value1":True},
                {"value1":True},
                {"value1":True},
                {"value1":True},
                {"value1":True}
                ]
        result = action.run(action="test.text",
                parameters=list_params,
                paging_limit=5,
                sleep_time=0,
                result_expr=None)
        self.assertEquals(True, result[0])
