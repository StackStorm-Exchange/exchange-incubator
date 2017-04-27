#!/usr/bin/env python

from st2actions.runners.pythonrunner import Action
import requests
import zipfile
from os import path, makedirs
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class DownloadArchive(Action):
    def run(self, url, save_as, verify_ssl, headers=None, params=None):
        save_path = path.split(save_as)[0]

        if not path.exists(save_path):
            makedirs(save_path)

        response = requests.get(url, headers=headers or {}, params=params or {}, verify=verify_ssl)
        if response.status_code != 200:
            return False, {'archive': '', 'error': response.text}

        try:
            with open(save_as, 'wb') as archive_fd:
                for chunk in response.iter_content(chunk_size=1024):
                    if not chunk:
                        continue

                    archive_fd.write(chunk)
        except zipfile.BadZipfile:
            pass

        return True, {'archive': save_as}
