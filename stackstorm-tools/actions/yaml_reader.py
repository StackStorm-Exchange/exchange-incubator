#!/usr/bin/env python

from st2actions.runners.pythonrunner import Action
import yaml


class YAMLReader(Action):
    def run(self, filename):
        with open(filename) as input_file:
            e = yaml.load(input_file)

        return True, e
