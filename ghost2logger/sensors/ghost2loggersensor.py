"""
Copyright 2017 David Gee

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

import eventlet
import json
from st2client.models import KeyValuePair
from requests.auth import HTTPBasicAuth
from base64 import b64encode
from requests.auth import HTTPBasicAuth
from st2reactor.sensor.base import Sensor
from flask import request, json, Flask, Response
from functools import wraps

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)


_username = ""
_password = ""


def authenticate():
    """Send a 401 response that enables basic auth."""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def check_auth(username, password):
    """Check if a username and password combo is valid."""
    return username == _username and password == _password


def requires_auth(f):
    """Wrapper function."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


class Ghost2loggerSensor(Sensor):
    """This Sensor sets up the GhOST2Logger Service base information."""

    def __init__(self, sensor_service, config=None):
        """Stuff."""
        super(Ghost2loggerSensor, self).__init__(sensor_service, config)

        self._logger = self._sensor_service.get_logger(__name__)

        self._sensor_listen_ip = self._config.get('sensor_listen_ip',
                                                  '0.0.0.0')

        self._sensor_listen_port = self._config.get('sensor_listen_port',
                                                    '12021')

        self._username = self._config.get('username', 'admin')
        self._password = self._config.get('password', 'admin')
        self._st2_api_key = self._config.get('st2_api_key', None)

        # Now set the global username and passwords for auth
        global _username
        global _password

        _username = self._username
        _password = self._password

        self._pmatch = 'ghost2logger.pattern_match'

        self._app = Flask(__name__)

    def setup(self):
        """Here we handle spawning the GO service and managing it."""
        # 1. Check for PID KEY
        # 2. Attempt to kill existing GhOST2Loggers
        # 3. Spawn new and register PID. Pass as arguments:
        #             API_KEY, SENSOR_PORT, GO_PORT, SENSOR_VERSION
        pass

    def run(self):
        """Run the app."""
        if not self._st2_api_key:
            raise Exception('[ghost2logger_sensor]: _st2_api_key not set')

        if not self._username:
            raise Exception('[ghost2logger_sensor]: _username not set')

        if not self._password:
            raise Exception('[ghost2logger_sensor]: _password not set')

        # Routes
        @self._app.route('/patternmatch/', methods=['PUT'])
        @requires_auth
        def process_incoming():
            status = self._process_request(request)
            response = Response(status[0], status=status[1])
            return response

        # Start the Flask App
        self._logger.info('[Ghost2logger]: Calling Flask App')

        self._app.run(host=self._sensor_listen_ip,
                      port=self._sensor_listen_port)

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

    def _process_request(self, request):
        self._logger.info('[Ghost2logger]: Received Request')
        if request.headers['Content-Type'] == 'application/json':
            payload = request.json
            if 'pattern' and 'host' and 'message' in payload:
                self._logger.info(request.json)
                self._logger.debug('[ghost2logger_sensor]: processing request {}'.
                                   format(payload))

                self._sensor_service.dispatch(trigger=self._pmatch,
                                              payload=payload)
                return ('ok', 200)
            else:
                return ('fail', 415)
        else:
            return ('fail', 415)
