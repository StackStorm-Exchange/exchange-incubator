import openai

from st2common.runners.base_action import Action


class ImageGeneration(Action):
    def run(self, query, size):
        config = self.config
        openai.api_key = config.get("openai_token")
        openai.organization = config.get("openai_org")
        return openai.Image.create(prompt=query, size=size)
