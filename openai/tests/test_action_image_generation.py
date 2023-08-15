from st2tests.base import BaseActionTestCase
from openai.openai_object import OpenAIObject

import image_generation
import mock

__all__ = ["TestChatCompletion"]


class TestChatCompletion(BaseActionTestCase):
    action_cls = image_generation.ImageGeneration

    @mock.patch("chat_completion.openai.Image.create")
    def test_image_generation_makes_valid_image_generation_request(self, mock_openai):
        mock_openai.return_value = OpenAIObject()
        action = self.get_action_instance()
        action.run("fake query", "512x512")
        mock_openai.assert_called_with(prompt="fake query", size="512x512")
