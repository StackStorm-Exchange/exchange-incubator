#!/usr/bin/env python

from st2actions.runners.pythonrunner import Action
import zipfile
from os import path, makedirs


class UnzipArchive(Action):
    def run(self, archive, unzip_path, list_content=False):
        if unzip_path.startswith('/'):
            unzip_abspath = unzip_path
        else:
            unzip_abspath = path.join(path.abspath(path.curdir), unzip_path)

        if not path.exists(unzip_abspath):
            makedirs(unzip_abspath)

        zip_ref = zipfile.ZipFile(archive, 'r')
        zip_ref.extractall(unzip_abspath)
        payload = {'unzip_path': unzip_abspath}

        if list_content:
            payload['content'] = zip_ref.namelist()
        else:
            payload['content'] = []

        zip_ref.close()

        return True, payload
