import openai

from st2common.runners.base_action import Action


class ChatCompletion(Action):
    def run(self, query, model):
        config = self.config
        openai.api_key = config.get("openai_token")
        openai.organization = config.get("openai_org")
        return openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": query}
            ]
        )
