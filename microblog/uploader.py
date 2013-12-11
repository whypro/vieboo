# -*- coding: utf-8 -*-
__author__ = 'whypro'
import os
import hashlib
import pybcs
from flask import current_app


IMAGES = tuple('jpg jpe jpeg png gif svg bmp'.split())


class Uploader(object):
    def remove(self, filename):
        # raise UnimplementError
        pass

    def save(self, storage):
        # raise UnimplementError
        pass

    def generate_random_basename(self, file_data):
        return hashlib.md5(file_data).hexdigest()

    def validate_extensions(self, filename, allowed):
        return '.' in filename and filename.rsplit('.', 1)[1] in allowed


class LocalUploader(Uploader):
    def remove(self, basename):
        dirname = current_app.config['UPLOADS_DIR']
        fullname = os.path.join(dirname, basename)
        try:
            os.remove(fullname)
        except OSError as e:
            pass

    def save(self, storage):
        file_data = storage.read()
        filename = self.generate_random_basename(file_data)
        ext = storage.filename.rsplit('.', 1)[1]
        basename = '%s.%s' % (filename, ext)
        dirname = current_app.config['UPLOADS_DIR']
        fullname = os.path.join(dirname, basename)
        # Local
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        f = open(fullname, 'wb')
        f.write(file_data)
        f.close()
        # storage.save(fullname)
        return basename


class BCSUploader(Uploader):
    def remove(self, basename):
        dirname = '/'
        fullname = os.path.join(dirname, basename)

        # BAE BCS
        baebcs = self.create_bcs()
        # 假设 bucket 已创建
        bucket = baebcs.bucket(current_app.config['BCS_BUCKET_NAME'])
        obj = bucket.object(str(fullname))  # 此处一定要加 str()，否则会出现 UnicodeDecodeError
        obj.delete()

    def uri(self, basename):
        dirname = '/'
        fullname = os.path.join(dirname, basename)
        return fullname

    def save(self, storage):
        file_data = storage.read()
        filename = self.generate_random_basename(file_data)
        ext = storage.filename.rsplit('.', 1)[1]
        basename = '%s.%s' % (filename, ext)
        dirname = '/'
        fullname = os.path.join(dirname, basename)

        # BAE BCS
        baebcs = self.create_bcs()
        # 假设 bucket 已创建
        bucket = baebcs.bucket(current_app.config['BCS_BUCKET_NAME'])
        obj = bucket.object(str(fullname))  # 此处一定要加 str()，否则会出现 UnicodeDecodeError
        obj.put(file_data)
        return basename

    # For BAE
    def create_bcs(self):
        bcs = pybcs.BCS(
            current_app.config['BCS_ADDR'],
            current_app.config['BCS_ACCESS_KEY'],
            current_app.config['BCS_SECRET_KEY'],
        )
        return bcs