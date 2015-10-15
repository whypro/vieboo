# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import hashlib

from flask import current_app


__author__ = 'whypro'


class InvalidFileException(Exception):
    pass


class Uploader(object):
    def remove(self, filename):
        raise NotImplementedError

    def save(self, storage):
        raise NotImplementedError

    @staticmethod
    def sha1(data):
        """
            根据文件生成 sha1 值
        """
        return hashlib.sha1(data).hexdigest()

    @staticmethod
    def is_valid_ext(filename, allowed):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

    @staticmethod
    def is_valid_size(data):
        # print len(data)
        # print current_app.config['MAX_CONTENT_LENGTH']
        return len(data) < current_app.config['MAX_CONTENT_LENGTH']

    def save(self, storage):
        file_data = storage.read()
        if not self.is_valid_ext(storage.filename, current_app.config['IMAGE_EXT']) or not self.is_valid_size(file_data):
            raise InvalidFileException
        filename = self.sha1(file_data)
        ext = storage.filename.rsplit('.', 1)[1]
        basename = '%s.%s' % (filename, ext)
        fullname = os.path.join(self.dirname, basename)
        self._store(fullname, file_data)
        return basename

    def _store(self, fullname, data):
        raise NotImplementedError


class LocalUploader(Uploader):
    def __init__(self):
        self.dirname = os.path.abspath(current_app.config['UPLOADS_DIR'])
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

    def remove(self, basename):
        fullname = os.path.join(self.dirname, basename)
        try:
            os.remove(fullname)
        except OSError as e:
            print '文件不存在'
            # raise e

    def _store(self, fullname, data):
        # Local
        f = open(fullname, 'wb')
        f.write(data)
        f.close()

