# Copyright (C) 2020 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
# The contents of this software are proprietary and confidential
# to the Hewlett Packard Enterprise Development LP. No part of this
# program may be photocopied, reproduced, or translated into another
# programming language without prior written consent of the
# Hewlett Packard Enterprise Development LP.


from requests import post
from tornado import escape
import json
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.websocket import websocket_connect
from tornado.httpclient import HTTPRequest
import sys
from ssl import PROTOCOL_SSLv23
import asyncio
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
import uuid
import eventlet


class Client(object):
    def __init__(self, url, timeout, sensor, ip_address, username, password,
                 interface, proxy=None):
        self.sensor = sensor
        self.url = url
        self.timeout = timeout
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.interface = interface
        if proxy is None:
            self.proxy = {'http': None, 'https': None}
        else:
            self.proxy = proxy

        if isinstance(interface, list):
            self.subscribe_uri = []
            for port in interface:
                self.subscribe_uri.append(self._create_url(port))
        else:
            self.subscribe_uri = self._create_url(interface)

    def establish_connection(self):
        asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.cookie_header = self.login(self.ip_address, self.username,
                                        self.password, proxies=self.proxy)
        self.connect(self.url, self.cookie_header)
        self.ioloop.start()

    @gen.coroutine
    def connect(self, ws_uri, cookie_header):
        print("trying to connect")
        try:
            http_request = HTTPRequest(url=ws_uri,
                                       headers=cookie_header,
                                       follow_redirects=True,
                                       ssl_options={"ssl_version":
                                                    PROTOCOL_SSLv23},
                                       validate_cert=False)
            self.ws = yield websocket_connect(http_request)
        except Exception as e:
            print("connection error" + str(e))
        else:
            print("connected")
            self.run()

    @gen.coroutine
    def run(self):
        topics = []
        if isinstance(self.subscribe_uri, list):
            for uri in self.subscribe_uri:
                topics.append({"name": uri})
        else:
            topics.append({"name": self.subscribe_uri})

        message = escape.utf8(json.dumps({"topics": topics,
                                          "type": "subscribe"}))
        self.ws.write_message(message)
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                self.sensor._logger.warn('[AOSCXPortSensor]: Connection to '
                                         '{0} lost - exiting...'
                                         ''.format(self.ip_address))
                sys.exit(-1)
            else:
                msg_in_json = self._check_if_json(msg)
                if msg_in_json is not None:
                    success_test = self._check_if_success(msg_in_json)
                    if success_test:
                        if self._make_trigger(msg_in_json) is not None:
                            trigger_name = self.sensor._trigger
                            trigger_paylog = self._make_trigger(msg_in_json)
                            trace_tag = uuid.uuid4().hex
                            self.sensor.sensor_service.dispatch(trigger_name,
                                                                trigger_paylog,
                                                                trace_tag)
                    else:
                        self.sensor.sensor_service.get_logger().warn()

    def _create_url(self, interface):
        interface_encoded = interface.replace(":", "%3A").replace("/", "%2F")
        uri = "/rest/v1/system/ports/{0}".format(interface_encoded)
        self.sensor._logger.debug('[AOSCXPortSensor]: Subscribe '
                                  'to URI {0}...'.format(uri)
                                  )
        return uri

    # Makes a trigger from a JSON object
    def _make_trigger(self, msg_in_json):
        values_dict = msg_in_json["data"][0]["resources"][0]["values"]
        if "admin" in values_dict:
            return {"admin": str(values_dict["admin"])}
        else:
            return None

    # Checks if a message is JSON
    def _check_if_json(self, result):
        try:
            msg_json = json.loads(result)
        except ValueError:
            print("The message received is not a valid JSON")
        return msg_json

    def _check_if_success(self, json_response):
        pass_type = False
        if "type" in json_response:
            type_msg = json_response["type"]
            if type_msg == "success":
                pass_type = True
        if "data" in json_response:
            for each in json_response['data']:
                if isinstance(self.subscribe_uri, list):
                    for uri in self.subscribe_uri:
                        if uri in each['topicname']:
                            pass_type = True
                            if "resources" in json_response['data']:
                                pass_type = True
                else:
                    if self.subscribe_uri in each['topicname']:
                        pass_type = True
                        if "resources" in json_response['data']:
                            pass_type = True
        return pass_type

    # Logs into the specified AOS-CX switch
    def login(self, switch_ip, username, password,
              proxies=None):
        if proxies is None:
            proxies = {'http': None, 'https': None}
        # Force to provide a password if a username is provided
        if username is None or password is None:
            self.sensor._logger.warn('[AOSCXPortSensor]: Must provide username'
                                     ' and password for Login...')
            exit(-1)

        params = {'username': username,
                  'password': password}
        login_url = 'https://'+switch_ip+':443/rest/v1/login'
        login_header = {'Content-Type': 'application/x-ww-form-urlencoded'}
        for i in range(self.timeout):
            response = post(login_url, verify=False, headers=login_header,
                            params=params, proxies=proxies)
            if response.status_code != 200:
                print("failed to connect code {0} - "
                      "{1}\n retry {2}/10sec"
                      "".format(response.status_code,
                                response.text, i))
                self.sensor._logger.warn('[AOSCXPortSensor]: Login '
                                         'failed...'
                                         '\nStatus Code{0} - {1}'
                                         ''.format(response.status_code,
                                                   response.text))
                eventlet.sleep(1.0)
            else:
                print("login successful")
                self.sensor._logger.debug('[AOSCXPortSensor]: Login '
                                          'successful...')
                cookie_header = {'Cookie': response.headers['set-cookie']}
                return cookie_header
        err_msg = ('[AOSCXPortSensor]: Login failed...'
                   '\nStatus Code{0} - {1}'.format(response.status_code,
                                                   response.text))
        self.sensor._logger.warn(err_msg)
        exit(err_msg)

    def logout(self):
        logout_url = 'https://' + self.ip_address + ':443/rest/v1/logout'
        logout_header = {'Content-Type': 'application/x-ww-form-urlencoded'}
        response = post(logout_url, verify=False, headers=logout_header,
                        proxies=self.proxy)
        if response.status_code != 200:
            self.sensor._logger.debug('[AOSCXPortSensor]: Logout failed...\n'
                                      'Status Code{0} - {1}'
                                      ''.format(response.status_code,
                                                response.text))
        else:
            self.sensor._logger.debug('[AOSCXPortSensor]: Logout '
                                      'successful...')
