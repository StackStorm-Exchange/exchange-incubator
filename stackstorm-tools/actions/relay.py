#!/usr/bin/env python

from st2actions.runners.pythonrunner import Action


class Relay(Action):
    def run(self, objects):
        return True, objects
