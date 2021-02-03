from st2common.runners.base_action import Action
import paho.mqtt.publish as publish
import time
import csv
import json


class PublishCsvDataAction(Action):
    def __init__(self, config):
        super(PublishCsvDataAction, self).__init__(config)

        self._config = self.config

        self._client = None
        self._tenant_id = self._config.get('tenant_id', None)
        self._hostname = self._tenant_id + "." + self._config.get('hostname', None)
        self._port = self._config.get('port', 1883)
        self._protocol = self._config.get('protocol', 'MQTTv311')
        self._client_id = self._config.get('client_id', None)
        self._userdata = self._config.get('userdata', None)
        self._username = self._config.get('username', None)
        self._password = self._config.get('password', None)
        self._subscribe = self._config.get('subscribe', None)
        self._csvFilePath = self._config.get('csvFilePath', None)
        self._ssl = self._config.get('ssl', False)
        self._ssl_cacert = self._config.get('ssl_cacert', None)
        self._ssl_cert = self._config.get('ssl_cert', None)
        self._ssl_key = self._config.get('ssl_key', None)

        self._ssl_payload = None
        self._auth_payload = None

        if not self._csvFilePath:
            raise ValueError('Missing CSV data file path in config file')

    def run(self, topic, qos=0, retain=False):
        if self._username:
            self._auth_payload = {
                'username': self._username,
                'password': self._password,
            }

        if self._ssl:
            if not self._ssl_cacert:
                raise ValueError('Missing "ssl_cacert" config option')

            if not self._ssl_cert:
                raise ValueError('Missing "ssl_cert" config option')

            if not self._ssl_key:
                raise ValueError('Missing "ssl_key" config option')

            self._ssl_payload = {
                'ca_certs': self._ssl_cacert,
                'certfile': self._ssl_cert,
                'keyfile': self._ssl_key,
            }
        self.logger.info('Reading CSV File ..')
        self.logger.debug(self._csvFilePath)
        List = []
        with open(self._csvFilePath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for rows in csvReader:
                List.append(rows)
        self.logger.info('Publishing data to via Mqtt ..')
        self.logger.debug("Topic : {}".format(topic))
        msg = {}
        for row in List:
            msg['d'] = row
            json_msg = json.dumps(msg, indent=4)
            self.logger.debug("Payload : {}".format(json_msg))
            publish.single(topic, payload=json_msg, qos=qos, retain=retain,
                       hostname=self._hostname, port=self._port,
                       client_id=self._client_id, keepalive=120,
                       auth=self._auth_payload, tls=self._ssl_payload,
                       protocol=self._protocol)
            time.sleep(0.1)
        self.logger.info('Action Completed Successfully')
