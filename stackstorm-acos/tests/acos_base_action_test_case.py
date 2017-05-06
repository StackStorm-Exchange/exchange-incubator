import logging
import yaml

from st2tests.base import BaseActionTestCase


class ACOSBaseActionTestCase(BaseActionTestCase):
    __test__ = False

    def setUp(self):
        super(ACOSBaseActionTestCase, self).setUp()

        self._full_config = yaml.safe_load(self.get_fixture_content('full.yml'))
        self._log_handler = self.LogHandler()

    class LogHandler(logging.StreamHandler):
        """Mock logging handler to check log output"""

        def __init__(self, *args, **kwargs):
            self.reset()
            logging.StreamHandler.__init__(self, *args, **kwargs)

        def emit(self, record):
            self.messages[record.levelname.lower()].append(record.getMessage())

        def reset(self):
            self.messages = {
                'debug': [],
                'info': [],
                'warning': [],
                'error': [],
                'critical': [],
            }
