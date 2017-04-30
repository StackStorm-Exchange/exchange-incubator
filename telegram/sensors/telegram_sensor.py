import telegram
from st2reactor.sensor.base import PollingSensor

class TelegramSensor(PollingSensor):
    def __init__(self, sensor_service, config, poll_interval):
       super(TelegramSensor, self).__init__(sensor_service=sensor_service,
                                            config=config,
                                            poll_interval=poll_interval)
       self._trigger_name = 'new_update'
       self._trigger_pack = 'telegram'
       self._trigger_ref = '.'.join([self._trigger_pack, self._trigger_name])


    def setup(self):
        self._client = telegram.Bot(token=self._config['apikey'])
        self._last_id = None

    def poll(self):
        if not self._last_id:
            updates = self._client.getUpdates()
        else:
            updates = self._client.getUpdates(offset=self._last_id+1)

        if updates:
            for u in updates:
                self._dispatch_trigger(u.to_dict())
            self._last_id = updates[-1].update_id

    def update_trigger(self):
        pass

    def add_trigger(self, trigger):
        pass

    def cleanup(self):
        pass

    def remove_trigger(self):
        pass

    def _dispatch_trigger(self, update):
        trigger = self._trigger_ref
        self._sensor_service.dispatch(trigger, update)
