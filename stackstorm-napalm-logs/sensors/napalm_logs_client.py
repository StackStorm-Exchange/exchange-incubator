import zmq
import napalm_logs.utils

from st2reactor.sensor.base import Sensor


class NapalmLogsSensor(Sensor):

    def __init__(self, sensor_service, config):

        super(NapalmLogsSensor, self).__init__(sensor_service, config)

        self._server_address = self.config.get('server_address')  # --publish-address
        self._server_port = self.config.get('server_port')           # --publish-port
        self._auth_address = self.config.get('auth_address')    # --auth-address
        self._auth_port = self.config.get('auth_port')             # --auth-port
        self._certificate = self.config.get('certificate_file')  # --certificate

    def setup(self):

        # Using zmq
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect('tcp://{address}:{port}'.format(address=self._server_address,
                                                       port=self._server_port))
        self.socket.setsockopt(zmq.SUBSCRIBE, b'')

        self.auth = napalm_logs.utils.ClientAuth(self._certificate,
                                                 address=self._auth_address,
                                                 port=self._auth_port)

    def run(self):

        while True:
            raw_object = self.socket.recv()
            decrypted = self.auth.decrypt(raw_object)
            self._sensor_service.dispatch(trigger='napalm_logs.log', payload=decrypted)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        # This method is called when trigger is created
        pass

    def update_trigger(self, trigger):
        # This method is called when trigger is updated
        pass

    def remove_trigger(self, trigger):
        # This method is called when trigger is deleted
        pass
