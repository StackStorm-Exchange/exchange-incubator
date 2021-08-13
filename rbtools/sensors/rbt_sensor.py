import datetime

from rbtools.api.client import RBClient
from st2reactor.sensor.base import PollingSensor

REVIEWBOARD_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class ReviewboardSensor(PollingSensor):
    '''
    Sensor will monitor for any new projects created in Reviewboard and
    emit trigger instance when one is created.
    '''
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(ReviewboardSensor, self).__init__(sensor_service=sensor_service,
                                                config=config,
                                                poll_interval=poll_interval)
        self._reviewboard_url = None
        self._logger = self._sensor_service.get_logger(__name__)
        # The Consumer Key created while setting up the
        # "Incoming Authentication" in JIRA for the Application Link.
        self._last_message_timestamp = None
        self._poll_interval = 30
        self._rbt_client = None
        self._rbtools_root = None
        self._trigger_name = 'review_tracker'
        self._trigger_pack = 'rbtools'
        self._trigger_ref = '.'.join([self._trigger_pack, self._trigger_name])

    def setup(self):

        self._poll_interval = self._config.get(
            'poll_interval', self._poll_interval)
        self._reviewboard_url = self._config['url']

        options = {
            'server': self._config['url'],
            'verify_ssl': self._config['verify'],
            'allow_caching': self._config['allow_caching'],
            'in_memory_cache': self._config['in_memory_cache'],
            'save_cookies': self._config['save_cookies'],
        }

        auth_method = self._config['auth_method']

        if auth_method == 'token':
            options['api_token'] = self._config['api_token']
        elif auth_method == 'basic':
            options['username'] = self._config['username']
            options['password'] = self._config['password']
        else:
            msg = ('You must set auth_method to either "token"',
                   'or "basic" your rbtools.yaml config file.')
            raise Exception(msg)

        self._rbt_client = RBClient(self._reviewboard_url, **options)
        self._rbtools_root = self._rbt_client.get_root()

    def poll(self):
        self._detect_new_reviews()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _detect_new_reviews(self):
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(seconds=self._poll_interval)
        self._logger.info(f"Start Date - {start_date}, End Date - {end_date}")
        new_reviews = self._rbtools_root.get_review_requests(
            last_updated_from=start_date.strftime(REVIEWBOARD_DATE_FORMAT),
            last_updated_to=end_date.strftime(REVIEWBOARD_DATE_FORMAT),
            max_results=50, start=0)

        for review in new_reviews:
            self._dispatch_reviews_trigger(review)

    def _dispatch_reviews_trigger(self, review):

        payload = dict()

        payload['id'] = review.id
        payload['submitter'] = review.links.submitter.title
        payload['status'] = review.status
        payload['summary'] = review.summary
        payload['description'] = review.description
        payload['issue_open_count'] = review.issue_open_count
        payload['ship_it_count'] = review.ship_it_count
        payload['approved'] = review.approved
        payload['url'] = review.absolute_url
        payload['bugs_closed'] = [bug for bug in review.bugs_closed]

        self._sensor_service.dispatch(self._trigger_ref, payload)
