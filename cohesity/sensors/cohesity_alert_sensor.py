from cohesity_management_sdk.cohesity_client import CohesityClient
from st2reactor.sensor.base import PollingSensor


class CohesityAlertSensor(PollingSensor):
    def __init__(self, sensor_service, config, poll_interval):
        super(CohesityAlertSensor, self).__init__(
            sensor_service=sensor_service,
            config=config,
            poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(
            name=self.__class__.__name__)

    def setup(self):
        hostname = self._config['hostname']
        username = self._config['username']
        password = self._config['password']
        domain = self._config['domain']
        self._client = CohesityClient(hostname, username, password, domain)
        self._last_id = None

    def _get_last_id(self):
        if not self._last_id and hasattr(self._sensor_service, 'get_value'):
            self._last_id = self._sensor_service.get_value(
                name='cohesity.last_alert_id')
        return self._last_id

    def _set_last_id(self, last_id):
        self._last_id = last_id
        if hasattr(self._sensor_service, 'set_value'):
            self._sensor_service.set_value(
                name='cohesity.last_alert_id', value=last_id)

    def poll(self):
        # Get the newest alerts
        alerts = self._client.alerts.get_alerts(max_alerts=1000)
        if alerts:
            if not self._get_last_id():
                self._logger.debug('Last alert id not set')
                self._set_last_id(last_id=alerts[0].id)
                for a in alerts:
                    payload = {
                        'id': a.id,
                        'name': a.alert_document.alert_name,
                        'description': a.alert_document.alert_description,
                        'cause': a.alert_document.alert_cause,
                        'code': a.alert_code,
                        'state': a.alert_state,
                        'severity': a.severity,
                        'alert_type': a.alert_type,
                        'category': a.alert_category
                    }
                    self.sensor_service.dispatch(trigger='cohesity.new_alert',
                                                 payload=payload,
                                                 trace_tag=a.id)
            else:
                if alerts[0].id != self._get_last_id():
                    self._logger.debug('Found new alerts')
                    for a in alerts:
                        if a.id == self._get_last_id():
                            break
                        else:
                            payload = {
                                'id': a.id,
                                'name': a.alert_document.alert_name,
                                'description':
                                    a.alert_document.alert_description,
                                'cause': a.alert_document.alert_cause,
                                'code': a.alert_code,
                                'state': a.alert_state,
                                'severity': a.severity,
                                'alert_type': a.alert_type,
                                'category': a.alert_category
                            }
                            self.sensor_service.dispatch(
                                trigger='cohesity.new_alert',
                                payload=payload,
                                trace_tag=a.id)
                    # Set the last seen alert id
                    self._set_last_id(last_id=alerts[0].id)

    def cleanup(self):
        # This is called when the st2 system goes down.
        # Perform cleanup operations like closing the connections here.
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
