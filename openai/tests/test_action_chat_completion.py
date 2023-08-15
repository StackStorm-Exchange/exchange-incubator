from st2tests.base import BaseActionTestCase
from openai.openai_object import OpenAIObject

import chat_completion
import mock

__all__ = ["TestChatCompletion"]


class TestChatCompletion(BaseActionTestCase):
    action_cls = chat_completion.ChatCompletion

    @mock.patch("chat_completion.openai.ChatCompletion.create")
    def test_chat_completion_makes_valid_chat_completion_request(self, mock_openai):
        mock_openai.return_value = OpenAIObject()
        action = self.get_action_instance()
        action.run("fake query", "mock_model")
        mock_openai.assert_called_with(
            model="mock_model", messages=[{"role": "user", "content": "fake query"}]
        )
