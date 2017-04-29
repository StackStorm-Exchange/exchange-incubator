"""
Copyright 2017 David Gee.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


# See ../requirements.txt


# import json
# from requests.auth import HTTPBasicAuth
# import base64
import requests
from st2reactor.sensor.base import PollingSensor


class Ghost2loggerLoopback(PollingSensor):
    """This Sensor sets up the GhOST2Logger Service base information."""

    def __init__(self, sensor_service, config=None, poll_interval=None):
        """Stuff."""
        super(Ghost2loggerLoopback, self).__init__(sensor_service, config,
                                                   poll_interval)

        self._logger = self._sensor_service.get_logger(__name__)

        self._username = self._config.get('username')
        self._password = self._config.get('password')
        # self._authkey = self._username + ":" + self._password
        # self._authkey = base64.b64encode(self._authkey)
        # self._authkey = "Basic " + self._authkey
        # self._logger.info('[Ghost2logger] authkey = ' + self._authkey)
        self._st2_api_key = self._config.get('st2_api_key', None)
        self._st2url = self._config.get('st2url')

        self._ghost_listen_ip = self._config.get('ghost_ip')
        self._ghost_listen_port = self._config.get('ghost_port')

        if self._ghost_listen_ip == '0.0.0.0':
            self._ghost_url = 'http://127.0.0.1:' + \
                str(self._ghost_listen_port)
        else:
            self._ghost_url = 'http://' + self._ghost_listen_ip + \
                ":" + str(self._ghost_listen_port)

        self._logger.info('[Ghost2logger] _ghost2_url = ' + self._ghost_url)

        self._ghost2loggerGUID = ""
        self._rules = {}

    def setup(self):
        """Stuff."""
        pass

    def poll(self):
        """Poll the APIs."""
        if not self._st2_api_key:
            raise Exception('[ghost2logger_sensor]: _st2_apl_key not set')

        if not self._username:
            raise Exception('[ghost2logger_sensor]: _username not set')

        if not self._password:
            raise Exception('[ghost2logger_sensor]: _password not set')

        # Do the actual things here
        # 1. Check Ghost2logger GUID
        _tmp_guid = self._ghost2loggergetGUID()

        if _tmp_guid != self._ghost2loggerGUID:
            self._rules = {}
            self._ghost2loggergpurge()
            self._logger.info('[ghost2logger_sensor]: GUID does not match')
            self._logger.info('[ghost2logger_sensor]: purged')
            self._ghost2loggerGUID = _tmp_guid

        self._logger.info('[ghost2logger_sensor]: Ghost2logger GUID ' +
                          self._ghost2loggerGUID)

        # 2. Connect to API and get rules
        HEADERS = {"St2-Api-Key": self._st2_api_key}
        r = requests.get(self._st2url, headers=HEADERS, verify=False)
        _output_copy = r.json()
        self._process_rules(_output_copy)

    def cleanup(self):
        """Stuff."""
        pass

    def add_trigger(self, trigger):
        """Stuff."""
        pass

    def update_trigger(self, trigger):
        """Stuff."""
        pass

    def remove_trigger(self, trigger):
        """Stuff."""
        pass

    def _process_rules(self, rules_payload):
        """Process the rules payload."""
        # self._rules = {"1.1.1.1": ["thing", "boobs"]}
        _new = {}

        # _output = json.dumps(rules_payload)

        try:
            # 1. Sort rules in to rule dictionary
            for _rule in rules_payload:
                _host = _rule['criteria']['trigger.host']['pattern']
                if _host in _new:
                    _new[_host].append(_rule['criteria']['trigger.pattern']
                                       ['pattern'])
                else:
                    _new[_host] = []
                    _new[_host].append(_rule['criteria']['trigger.pattern']
                                       ['pattern'])

            # Check for key differences and delete the old stuff
            _deletekeys = set(self._rules.keys()).difference(set(_new.keys()))
            for each in _deletekeys:
                _json = {'Operation': 2, 'Host': each, 'Pattern': ['KEYDEL']}
                self._rest_process(_json)

            # At this point we have a dict of new rules, let's use as an index
            for key in _new:
                # Get a list of patterns for each host
                if key in self._rules:
                    _oldlist = self._rules[key]
                else:
                    _oldlist = []

                _newlist = _new[key]
                # First we check for deletions
                _to_delete = set(_oldlist).difference(set(_newlist))
                # Next we get additions
                _to_add = set(_newlist).difference(set(_oldlist))

                # Now we have the deletions
                for k in _to_delete:
                    # self._logger.info('[Ghost2logger]: Delete ' + key + ":"
                    #                  + str(k))

                    _json = {'Operation': 2, 'Host': str(key),
                             'Pattern': [str(k)]}
                    self._rest_process(_json)

                # Now we have the additions
                for k in _to_add:
                    # self._logger.info('[Ghost2logger]: Add ' + key + ":"
                    #                  + str(k))

                    _json = {'Operation': 1, 'Host': str(key),
                             'Pattern': [str(k)]}
                    self._rest_process(_json)

                # Once we've done this, the rules are the same
            self._rules = _new
        except Exception as e:
            self._logger.info('[Ghost2logger]: Issue with parsing rules: '
                              + str(e))
            return

    def _rest_process(self, _json):
        # Let's deal with the JSON API calls here
        self._logger.info('[Ghost2logger]: ' + str(_json))

        HEADERS = {"Content-Type": 'application/json'}

        _URL = self._ghost_url + "/v1/"
        requests.put(_URL, headers=HEADERS, verify=False, json=_json,
                     auth=(self._username, self._password))

    def _ghost2loggergetGUID(self):
        # Let's deal with the JSON API calls here

        HEADERS = {"Content-Type": 'application/json'}

        _URL = self._ghost_url + "/v1/guid"
        r = requests.get(_URL, headers=HEADERS, verify=False,
                         auth=(self._username, self._password))
        _data = r.json()
        if _data['host'] == "GUID":
            for _item in _data['pattern']:
                _guid = str(_item)

            return _guid
        else:
            return ""

    def _ghost2loggergpurge(self):
        # Let's deal with the JSON API calls here
        self._logger.info('[Ghost2logger]: Purge Ghost2logger')

        HEADERS = {"Content-Type": 'application/json'}

        _URL = self._ghost_url + "/v1/all"
        r = requests.delete(_URL, headers=HEADERS, verify=False,
                            auth=(self._username, self._password))

        _data = r.json()
        self._logger.info('[Ghost2logger]: Purged ghost2logger' + str(_data))
