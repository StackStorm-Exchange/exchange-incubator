import os
import time

from selenium import webdriver

from st2actions.runners.pythonrunner import Action

__all__ = [
    'CaptureScreenshotAction'
]


class CaptureScreenshotAction(Action):
    def run(self, url, window_size=(1024, 768), screenshot_path=None):
        executable_path = self.config.get('executable_path', None)

        if executable_path:
            self.logger.debug('Using PhantomJS executable from "%s"' % (executable_path))
            driver = webdriver.PhantomJS(executable_path=executable_path)
        else:
            driver = webdriver.PhantomJS()

        if window_size:
            self.logger.debug('Using window size %s' % (str(window_size)))
            driver.set_window_size(*tuple(window_size))

        driver.get(url)

        if not screenshot_path:
            file_name = 'screencap-%s.png' % (str(int(time.time())))
            screenshot_path = os.path.join('/tmp/', file_name)

        success = driver.save_screenshot(screenshot_path)

        if success:
            self.logger.debug('Screenshot saved to "%s"' % (screenshot_path))

        return (success, screenshot_path)
