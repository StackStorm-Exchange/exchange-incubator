import json
import requests
import sensor_constants as C
from flask import request, Flask
from st2reactor.sensor.base import Sensor

class LogicMonitorSensor(Sensor):
    def __init__(self, sensor_service, config=None):
        self._config = config
        self._sensor_service = sensor_service

        self._host = '0.0.0.0'
        self._port = '5000'

        if config != None:
            self._auth_enabled = config.get('auth_enabled')

        self._app = Flask(__name__)
        self._log = self._sensor_service.get_logger(__name__)

    def setup(self):
        pass

    def run(self):
        @self._app.route('/', methods=['POST'])
        def handle_webhook():

            # Get JSON data from POST request
            try:
                data = json.loads(request.data)
                self._log.info(C.LOG_LOADING_DATA)
            except Exception:
                self._log.info(C.LOG_FAILED_TO_PARSE_JSON)
                return C.RES_FAILED_TO_PARSE_JSON

            # Get API Key from POST request
            try:
                _apiKey = data[C.API_KEY_KEY]
                self._log.info(C.LOG_API_KEY_EXISTS)
            except Exception:
                self._log.info(C.LOG_API_KEY_DOES_NOT_EXIST)
                return C.RES_API_KEY_DOES_NOT_EXIST

            if self._auth_enabled is True:

                # Auth is enabled
                self._log.info(C.LOG_AUTH_ENABLED)

                # Create local GET Request to ensure StackStorm API Key exists and is enabled
                _headers = {'St2-Api-Key':_apiKey,'cache-control':'no-store'}

                # Send the GET Request & store response.
                _response = requests.get(url=C.AUTH_URL, headers=_headers, verify=False)

                # AUTHENTICATION STEP : Ensure response status-code is OK. Non-existent or disabled API Keys will fail here.
                _responseStatusCode = _response.status_code
                if _responseStatusCode != requests.codes.ok:

                    # Authentication failed : Bad response code
                    self._log.info(F'{C.LOG_FAILED_BAD_RESPONSE}{_response.text}')
                    return F'{C.RES_FAILED_BAD_RESPONSE}{_response.text}'

                # SUCCESS : Authentication succeeded. Inject trigger/payload & return response
                self._log.info(C.LOG_AUTH_SUCCEEDED)
                del data[C.API_KEY_KEY] # Remove API Key from payload before it is injected with the trigger
                self._sensor_service.dispatch(C.ALERT_TRIGGER, data)
                self._log.info(F'{C.LOG_TRIGGER_DISPATCHED}"{data}"')
                return C.RES_SUCCESS_AUTH_ENABLED

            elif self._auth_enabled is False:

                # Auth is disabled
                self._log.info(C.LOG_AUTH_DISABLED)

                # SUCCESS - Authentication disabled. Inject trigger/payload & return response
                del data[C.API_KEY_KEY] # Remove API Key from payload before it is injected with the trigger
                self._sensor_service.dispatch(C.ALERT_TRIGGER, data)
                self._log.info(F'{C.LOG_TRIGGER_DISPATCHED}"{data}"')
                return C.RES_SUCCESS_AUTH_DISABLED

            # Default response - this should never occur.
            self._log.info(C.LOG_DEFAULT_RESPONSE)
            return C.RES_DEFAULT_RESPONSE

        self._app.run(host=self._host, port=self._port)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass