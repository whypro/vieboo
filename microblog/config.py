# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import os
import platform

__all__ = ['LocalConfig', 'LocalDevelopmentConfig', 'BAEConfig', 'LocalDevelopmentBCSConfig']

class Config(object):
    SECRET_KEY = 'I love you.'
    MAX_CONTENT_LENGTH = 4 * 1024 *1024   # 上传文件大小：4MB
    PER_PAGE = 10
    IMAGE_EXT = tuple('jpg jpe jpeg png gif svg bmp'.split())
    USE_BCS_BUCKET = False
    SQLALCHEMY_POOL_RECYCLE = 10
    # FLASK-THEMES
    DEFAULT_THEME = 'newstyle'

    
class LocalConfig(Config):
    # 本地服务器配置
    # 数据库配置
    DB_HOST = 'localhost'
    DB_DATABASE = 'microblog'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'whypro'
    DB_PORT = int(3306)
    # FLASK-SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@{host}:{port}/{database}'.format(
        username=DB_USERNAME, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT,
        database=DB_DATABASE
    )
    
    TEMP_DIR = 'temp'
    UPLOADS_DIR = 'uploads'



class LocalDevelopmentConfig(LocalConfig):
    DEBUG = True


class HerokuConfig(Config):
    # 生产服务器配置
    # 数据库配置
    # FLASK-SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # TEMP_DIR = const.APP_TMPDIR

