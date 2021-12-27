# CONSTANTS USED IN "logicmonitor_sensor.py"

# Authentication
API_KEY_KEY = "apiKey"
AUTH_URL = "https://127.0.0.1/api/"

# Trigger
ALERT_TRIGGER = "logicmonitor.alert_trigger"

# Log constants
LOG_LOADING_DATA = "PAYLOAD JSON LOADED SUCCESSFULLY!"
LOG_FAILED_TO_PARSE_JSON = "DELIVERY NOT ACCEPTED! The webhook-sensor failed to parse the payload's body as JSON."
LOG_API_KEY_EXISTS = "PAYLOAD CONTAINS 'apiKey' FIELD!"
LOG_API_KEY_DOES_NOT_EXIST = "DELIVERY NOT ACCEPTED! The payload does not contain a required object with key 'apiKey'."
LOG_FAILED_BAD_RESPONSE = (
    "AUTHENTICATION FAILED! Webhook-sensor received bad response code from StackStorm: "
)
LOG_AUTH_ENABLED = "AUTHENTICATION IS ENABLED."
LOG_AUTH_SUCCEEDED = "AUTHENTICATION SUCCEEDED!"
LOG_AUTH_DISABLED = "AUTHENTICATION IS DISABLED! It is strongly recommended to enable authentication in your pack's configuration file!"
LOG_TRIGGER_DISPATCHED = 'Trigger/payload dispatched into StackStorm. trigger="logicmonitor.alert_trigger" , payload='
LOG_DEFAULT_RESPONSE = "Unknown error has occurred."

# HTTP Response Constants
RES_FAILED_TO_PARSE_JSON = "DELIVERY NOT ACCEPTED! The webhook-sensor failed to parse the payload's body as JSON."
RES_API_KEY_DOES_NOT_EXIST = "DELIVERY NOT ACCEPTED! The payload does not contain a required object with key 'apiKey'."
RES_FAILED_BAD_RESPONSE = (
    "AUTHENTICATION FAILED! Webhook-sensor received bad response code from StackStorm: "
)
RES_SUCCESS_AUTH_ENABLED = "SUCCESS! LogicMonitor has successfully authenticated with StackStorm. Trigger/payload injected into StackStorm."
RES_SUCCESS_AUTH_DISABLED = "SUCCESS! Trigger/payload injected into StackStorm. (AUTHENTICATION IS DISABLED! It is strongly recommended to enable authentication in your pack's configuration file!)"
RES_DEFAULT_RESPONSE = "Unknown error has occurred."
