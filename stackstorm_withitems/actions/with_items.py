import copy
import jinja2
import re
import os
import six
import time
import urllib3

from st2client.models import LiveAction
from st2client.client import Client
from st2client.commands import action as st2action
from st2common.runners.base_action import Action

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

JINJA_REGEXP = '({{(.*?)}})'

class WithItemsAction(Action):

    def __init__(self, config):
        super(WithItemsAction, self).__init__(config)
        self.jinja_env = jinja2.Environment()
        self.jinja_pattern = re.compile(JINJA_REGEXP)
        self.api_key = self.config.get("st2api_key", None)

        if self.api_key is not None:
            if os.environ.get("ST2_AUTH_TOKEN", None) is not None:
                del os.environ["ST2_AUTH_TOKEN"]
        self.client = Client(base_url=config["st2baseurl"],
                auth_url=config["st2authurl"],
                api_key=self.api_key,
                api_url=config["st2apiurl"]
                )

    def unescape_jinja(self, expr):
        if isinstance(expr, six.string_types):
            return self.unescape_jinja_str(expr)
        elif isinstance(expr, list):
            return self.unescape_jinja_list(expr)
        elif isinstance(expr, dict):
            return self.unescape_jinja_dict(expr)
        else:
            raise TypeError("Unable to escape jinja expression for type: {var}".format(var=str(type(expr))))

    def unescape_jinja_str(self, expr_str):
        expr_str = expr_str.replace("{_{", "{{")
        expr_str = expr_str.replace("}_}", "}}")
        return expr_str

    def unescape_jinja_list(self, expr_list):
        return [self.unescape_jinja(expr) for expr in expr_list ]

    def unescape_jinja_dict(self, expr_dict):
        for k, v in six.iteritems(expr_dict):
            expr_dict[k] = self.unescape_jinja(v)
        return expr_dict

    def render_jinja(self, context, expr):
        if isinstance(expr, six.string_types):
            return self.render_jinja_str(context, expr)
        elif isinstance(expr, list):
            return self.render_jinja_list(context, expr)
        elif isinstance(expr, dict):
            return self.render_jinja_dict(context, expr)
        else:
            raise TypeError("Unable to render Jinja expression for type: {}".format(type(expr)))

    def render_jinja_str(self, context, expr_str):
        # find all of the jinja patterns in expr_str
        patterns = self.jinja_pattern.findall(expr_str)

        # if the matched pattern matches the full expression, then pull out
        # the first group [0][1] which is the content between the {{ }}
        # then use this special rendering method
        if patterns[0][0] == expr_str:
            # we only have a single pattern, render it so that a native type
            # will be returned
            func = self.jinja_env.compile_expression(patterns[0][1], expr_str)
            return func(**context)
        else:
            # we have multiple patterns in one string so rendering it
            # "normallY" and this will return a string
            template = self.jinja_env.from_string(expr_str)
            return template.render(context)

    def render_jinja_list(self, context, expr_list):
        return [self.render_jinja(context, expr) for expr in expr_list]

    def render_jinja_dict(self, context, expr_dict):
        rendered = {}
        for k, expr in six.iteritems(expr_dict):
            rendered[k] = self.render_jinja(context, expr)
        return rendered

    def run(self, action, parameters, paging_limit, sleep_time, result=None, **kwargs):
        # unescape jinja
        result_expr = result
        if result_expr:
            result_expr = self.unescape_jinja(result_expr)

        running_ids = []
        finished = []
        param_index = 0
        success = True
        while len(finished) < len(parameters):
            # fill paging pool
            while len(running_ids) < paging_limit and \
                    len(parameters) != len(running_ids) + len(finished) : # end of list no more to page
                self.logger.debug("creating action index: " + str(param_index))
                execution = self.client.executions.create(
                    LiveAction(action=action,
                               parameters=parameters[param_index]))
                running_ids.append(execution.id)
                param_index+=1

            # sleep and wait for some work to be done
            time.sleep(sleep_time)

            # check for completed or failures
            execution_list = self.client.liveactions.query(id=",".join(running_ids))
            for e_updated in execution_list:
                if e_updated.status in st2action.LIVEACTION_COMPLETED_STATES:
                    if e_updated.status != st2action.LIVEACTION_STATUS_SUCCEEDED:
                        success = False
                    self.logger.debug("finished execution: " + str(e_updated.id))
                    running_ids.remove(e_updated.id)
                    finished.append(e_updated)

        # extract the information out of the output
        outputs = []
        for exe in finished:
            outputs.append({"status": copy.deepcopy(exe.status),
                            "result": copy.deepcopy(exe.__dict__["result"])})
        results = []
        if result_expr:
            for output in outputs:
                result = output["result"]
                result_context = {"_": {"result": result}}
                result = self.render_jinja(result_context, result_expr)
                results.append(result)
        else:
            results = outputs

        return (success, results)
