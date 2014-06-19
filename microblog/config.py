# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import os
import platform


class Config(object):
    SECRET_KEY = 'I love you.'

    MAX_CONTENT_LENGTH = 4 * 1024 *1024   # 上传文件大小：4MB
    PER_PAGE = 10
    IMAGE_EXT = tuple('jpg jpe jpeg png gif svg bmp'.split())
    USE_BCS_BUCKET = False
    SQLALCHEMY_POOL_RECYCLE = 10
    # FLASK-THEMES
    DEFAULT_THEME = 'newstyle'


class DevelopmentConfig(Config):
    DEBUG = True

    # 本地服务器配置
    # 数据库配置
    DB_HOST = 'localhost'
    DB_DATABASE = 'microblog'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'whypro'
    DB_PORT = int(3306)

    # FLASK-SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = \
        'mysql://{username}:{password}@{host}:{port}/{database}'.format(
            username=DB_USERNAME, password=DB_PASSWORD,
            host=DB_HOST, port=DB_PORT,
            database=DB_DATABASE
        )

    TEMP_DIR = 'temp'
    UPLOADS_DIR = 'uploads'


class DevelopmentBCSConfig(DevelopmentConfig):
    API_KEY = 'IBWv1TZbjHGeC3euOCWCKQBE'
    SECRET_KEY = '0QuvWjERsuDrwf6NntSe962SWPgGGj3o'
    # BAE BCS 配置
    USE_BCS_BUCKET = True
    BCS_ADDR = 'bcs.duapp.com'
    BCS_ACCESS_KEY = API_KEY
    BCS_SECRET_KEY = SECRET_KEY
    BCS_BUCKET_NAME = 'vieboo'


class BAEConfig(Config):
    # 生产服务器配置
    # 数据库配置
    API_KEY = 'IBWv1TZbjHGeC3euOCWCKQBE'
    SECRET_KEY = '0QuvWjERsuDrwf6NntSe962SWPgGGj3o'

    DB_HOST = 'sqld.duapp.com'
    DB_DATABASE = 'kHeMtkVTtzsGvfbmEtLU'
    DB_USERNAME = API_KEY
    DB_PASSWORD = SECRET_KEY
    DB_PORT = int(4050)
    # TEMP_DIR = const.APP_TMPDIR

    # BAE BCS 配置
    BCS_ADDR = 'bcs.duapp.com'
    BCS_ACCESS_KEY = API_KEY
    BCS_SECRET_KEY = SECRET_KEY
    BCS_BUCKET_NAME = 'vieboo'

    USE_BCS_BUCKET = True

    # FLASK-SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@{host}:{port}/{database}'.format(
        username=DB_USERNAME, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT,
        database=DB_DATABASE
    )













