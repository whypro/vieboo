# -*- coding: utf-8 -*-
__author__ = 'whypro'
import os
import hashlib
import pybcs
from flask import current_app


class Uploader(object):
    def remove(self, filename):
        raise NotImplementedError()

    def save(self, storage):
        raise NotImplementedError()

    @staticmethod
    def generate_random_basename(file_data):
        return hashlib.md5(file_data).hexdigest()

    @staticmethod
    def is_valid_ext(filename, allowed):
        return '.' in filename and filename.rsplit('.', 1)[1] in allowed

    @staticmethod
    def is_valid_size(data):
        print len(data)
        print current_app.config['MAX_CONTENT_LENGTH']
        return len(data) < current_app.config['MAX_CONTENT_LENGTH']


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
            raise e

    def save(self, storage):
        file_data = storage.read()
        if not self.is_valid_ext(storage.filename, current_app.config['IMAGE_EXT']) or not self.is_valid_size(file_data):
            return None
        filename = self.generate_random_basename(file_data)
        ext = storage.filename.rsplit('.', 1)[1]
        basename = '%s.%s' % (filename, ext)
        fullname = os.path.join(self.dirname, basename)
        # Local
        f = open(fullname, 'wb')
        f.write(file_data)
        f.close()
        # storage.save(fullname)
        return basename


class BCSUploader(Uploader):
    def __init__(self):
        self.bcs = self.create_bcs()
        # 假设 bucket 已创建
        self.bucket = self.bcs.bucket(current_app.config['BCS_BUCKET_NAME'])
        self.dirname = '/'

    def create_bcs(self):
        return pybcs.BCS(
            current_app.config['BCS_ADDR'],
            current_app.config['BCS_ACCESS_KEY'],
            current_app.config['BCS_SECRET_KEY'],
        )

    def remove(self, basename):
        fullname = os.path.join(self.dirname, basename)
        obj = self.bucket.object(str(fullname))  # 此处一定要加 str()，否则会出现 UnicodeDecodeError
        try:
            obj.delete()
        except pybcs.httpc.HTTPException as e:
            raise e

    def uri(self, basename):
        fullname = os.path.join(self.dirname, basename)
        return fullname

    def save(self, storage):
        file_data = storage.read()
        if not self.is_valid_ext(storage.filename, current_app.config['IMAGE_EXT']) or not self.is_valid_size(file_data):
            return None
        filename = self.generate_random_basename(file_data)
        ext = storage.filename.rsplit('.', 1)[1]
        basename = '%s.%s' % (filename, ext)
        fullname = os.path.join(self.dirname, basename)

        # BAE BCS
        obj = self.bucket.object(str(fullname))  # 此处要加 str()，否则会出现 UnicodeDecodeError
        obj.put(file_data)
        return basename



