import yaml
import json

from st2tests.base import BaseActionTestCase


class ActiveDirectoryBaseActionTestCase(BaseActionTestCase):
    __test__ = False

    def setUp(self):
        super(ActiveDirectoryBaseActionTestCase, self).setUp()

        self._config_good = self.load_yaml('config_good.yaml')
        self._config_blank = self.load_yaml('config_blank.yaml')
        self._config_partial = self.load_yaml('config_partial.yaml')

    def load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))

    def load_json(self, filename):
        return json.loads(self.get_fixture_content(filename))

    @property
    def config_good(self):
        return self._config_good

    @property
    def config_blank(self):
        return self._config_blank

    @property
    def config_partial(self):
        return self._config_partial
