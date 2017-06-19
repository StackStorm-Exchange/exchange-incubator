from st2actions.runners.pythonrunner import Action


class BaseExchangeAction(Action):
    def __init__(self):
        self.account = None