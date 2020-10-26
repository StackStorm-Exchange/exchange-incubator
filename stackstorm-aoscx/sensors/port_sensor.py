from st2reactor.sensor.base import Sensor
from aoscx_websocket import *


class PortSensor(Sensor):
    def __init__(self, sensor_service, config=None):
        super(PortSensor, self).__init__(sensor_service=sensor_service,
                                         config=config)
        self._logger = self.sensor_service.get_logger(
            name=self.__class__.__name__)
        self._logger.debug('[AOSCXPortSensor]: Config contents '
                           '{0} ...'.format(config)
                           )
        if 'device' in config:
            self.device = config['device']
        else:
            self._logger.debug(
                '[AOSCXPortSensor]: No Device found in '
                'config {0} ...'.format(config)
            )
            exit(-1)
        if 'credentials' in config:
            self.credentials = config['credentials']
        else:
            self._logger.debug('[AOSCXPortSensor]: No credentials '
                               'found in config {0} ...'.format(config)
                               )
            exit(-1)

    def setup(self):
        self._trigger = None
        self.client = None

    def run(self):
        try:
            if self.device is not None:
                if 'ip_address' not in self.device:
                    self._logger.debug('[AOSCXPortSensor]: No IP Address'
                                       ' found for device {0} ...'
                                       ''.format(self.device)
                                       )
                    exit(-1)
                if 'credentials' not in self.device:
                    self._logger.debug('[AOSCXPortSensor]: No IP Address '
                                       'found for device {0} ...'
                                       ''.format(self.device)
                                       )
                    exit(-1)
                else:
                    if self.device['credentials'] not in self.credentials:
                        self._logger.debug('[AOSCXPortSensor]: No Credential '
                                           'found for device {0} ...'
                                           ''.format(self.device)
                                           )
                        exit(-1)

                if 'proxy' in self.device:
                    for key, value in self.device['proxy'].items():
                        if value.lower() in ['none', 'null', 'n/a']:
                            self.device['proxy'][key] = None
                else:
                    self.device['proxy'] = None

                ws_url = ("wss://{0}:443/rest/v1/notification"
                          "".format(self.device['ip_address']))
                self.client = Client(url=ws_url,
                                     timeout=10, sensor=self,
                                     ip_address=self.device['ip_address'],
                                     username=self.credentials[
                                         self.device['credentials']][
                                         'username'],
                                     password=self.credentials[
                                         self.device['credentials']][
                                         'password'],
                                     interface=self.device['interface'],
                                     proxy=self.device['proxy'])
                self._logger.debug('[AOSCXPortSensor]: '
                                   'Connecting to client ...')

                self.client.establish_connection()
            else:
                self._logger.debug('[AOSCXPortSensor]: No device found in '
                                   'config aoscx.yaml ...')
                exit('[AOSCXPortSensor]: No device found in '
                     'config aoscx.yaml ...')
        except Exception as e:
            error_msg = ('Sensor "{0}" run method raised '
                         'an exception: {1}.'.format(self.__class__.__name__,
                                                     e)
                         )
            self._logger.warn(error_msg, exc_info=True)
            exit(error_msg)

    # Performs cleanup operations when st2 goes down
    def cleanup(self):
        if self.client is not None:
            self.client.logout()
            self._logger.debug('[AOSCXPortSensor]: Disconnecting '
                               'from client {0}...'
                               ''.format(self.client.ip_address))

    # Called when a trigger is created
    def add_trigger(self, trigger):
        self._trigger = trigger.get('ref', None)
        if not self._trigger:
            raise Exception('Trigger {0} did not contain a ref.'
                            ''.format(trigger))

    # Called when a trigger is updated
    def update_trigger(self, trigger):
        pass

    # Called when a trigger is deleted
    def remove_trigger(self, trigger):
        pass
