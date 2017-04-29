#!/usr/bin/env python

from zipfile import is_zipfile
from tarfile import is_tarfile
from os import path, makedirs
from lib.action import ExtractArchive
from lib.action import UnknownArchive


class Extract(ExtractArchive):
    def __init__(self, config):
        super(Extract, self).__init__(config=config)

    def run(self, archive, directory, files=False):
        if directory.startswith('/'):
            extract_abspath = directory
        else:
            extract_abspath = path.join(path.abspath(path.curdir), directory)

        if not path.exists(extract_abspath):
            makedirs(extract_abspath)

        if is_tarfile(archive):
            archive_path, archive_content = self.untar(archive, extract_abspath, files=files)

        elif is_zipfile(archive):
            archive_path, archive_content = self.unzip(archive, extract_abspath, files=files)

        else:
            raise UnknownArchive('Unknown archive type: {}'.format(archive))

        return True, {"archive": archive_path, "files": archive_content}
