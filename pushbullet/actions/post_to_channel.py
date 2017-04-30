from st2actions.runners.pythonrunner import Action
from pushbullet import Pushbullet


class PostToChannel(Action):
    def __init__(self, config):
        self.client = Pushbullet(config['apikey'])

    def get_channel(self, channel):
        return [c for c in self.client.channels if c.channel_tag == channel][0]

    def run(self, channel, message, subject=''):
        channel = self.get_channel(channel)
        return channel.push_note(subject, message)

