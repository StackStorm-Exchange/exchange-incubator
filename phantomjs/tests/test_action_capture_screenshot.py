import mock

from st2tests.base import BaseActionTestCase

from capture_screenshot import CaptureScreenshotAction

__all__ = [
    'CaptureScreenshotAction'
]


class CaptureScreenshotActionTestCase(BaseActionTestCase):
    action_cls = CaptureScreenshotAction

    @mock.patch('capture_screenshot.webdriver')
    def test_executable_path_provided(self, mock_webdriver):
        action = self.get_action_instance()
        action.config['executable_path'] = '/tmp/bar'
        result = action.run(url='http://www.example.com')

        self.assertTrue(result[0])
        self.assertTrue(mock_webdriver.PhantomJS.call_count, 1)
        self.assertEqual(mock_webdriver.PhantomJS.call_args[0], ())
        self.assertEqual(mock_webdriver.PhantomJS.call_args[1],
                         {'executable_path': '/tmp/bar'})

    @mock.patch('capture_screenshot.webdriver')
    def test_executable_path_not_provided(self, mock_webdriver):
        action = self.get_action_instance()
        result = action.run(url='http://www.example.com')

        self.assertTrue(result[0])
        self.assertTrue(mock_webdriver.PhantomJS.call_count, 1)
        self.assertEqual(mock_webdriver.PhantomJS.call_args[0], ())
        self.assertEqual(mock_webdriver.PhantomJS.call_args[1], {})

    @mock.patch('capture_screenshot.webdriver')
    def test_screenshot_path_provided(self, mock_webdriver):
        action = self.get_action_instance()
        result = action.run(url='http://www.example.com', screenshot_path='bar.png')

        self.assertTrue(result[0])
        self.assertEqual(result[1], 'bar.png')

    @mock.patch('capture_screenshot.webdriver')
    def test_screenshot_path_not_provided(self, mock_webdriver):
        action = self.get_action_instance()
        result = action.run(url='http://www.example.com')

        self.assertTrue(result[0])
        self.assertTrue('/tmp/' in result[1])
