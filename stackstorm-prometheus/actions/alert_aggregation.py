#!/usr/bin/env python

from st2actions.runners.pythonrunner import Action
from collections import defaultdict


class AlertAggretation(Action):
    def run(self, alerts, outer_label, inner_label):
        a = defaultdict(list)
        for alert in alerts:
            a[alert['labels'][outer_label]].append(alert['labels'][inner_label])

        return a
