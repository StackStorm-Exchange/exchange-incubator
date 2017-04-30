import telegram

from st2actions.runners.pythonrunner import Action

class TelegramSendMessageAction(Action):
    def run(self, message, chat_id):
        bot = telegram.Bot(token=self.config['apikey'])
        m = bot.sendMessage(text=message, chat_id=chat_id)
        return m
