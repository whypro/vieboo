# -*- coding:utf-8 -*-
import os
import platform


# FLASK
DEBUG = True
SECRET_KEY = 'I love you.'
MAX_CONTENT_LENGTH = 4 * 1024 *1024   # 上传文件大小：4MB


# 自定义
if platform.system() == 'Windows':
    UPLOADS_DIR = 'D:/uploads'  # 绝对路径
else:
# elif platform.system() == 'Linux': 
    UPLOADS_DIR = '/home/whypro/Workspace/Vieboo/uploads'  # 绝对路径
USE_BCS_BUCKET = False
PER_PAGE = 10


# 生产服务器配置
if 'SERVER_SOFTWARE' in os.environ:
    from bae.core import const
    # 数据库配置
    DB_HOST = const.MYSQL_HOST
    DB_DATABASE = 'ersVIiuGQNlnwijllSmh'
    DB_USERNAME = const.MYSQL_USER
    DB_PASSWORD = const.MYSQL_PASS
    DB_PORT = int(const.MYSQL_PORT)
    TEMP_DIR = const.APP_TMPDIR

    # BAE BCS 配置
    BCS_ADDR = const.BCS_ADDR
    BCS_ACCESS_KEY = const.ACCESS_KEY
    BCS_SECRET_KEY = const.SECRET_KEY
    BCS_BUCKET_NAME = 'vieboo'

    USE_BCS_BUCKET = True

# 本地服务器配置
else:
    # 数据库配置
    DB_HOST = 'localhost'
    DB_DATABASE = 'microblog'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'whypro'
    DB_PORT = int(3306)
    TEMP_DIR = 'temp'

    # BAE BCS 配置
    BCS_ADDR = 'bcs.duapp.com'
    BCS_ACCESS_KEY = 'AF28c466e7dd74686195abc876d4849b'
    BCS_SECRET_KEY = '2b2f8ac70616dbea89fc2ac2312de1a9'
    BCS_BUCKET_NAME = 'vieboo'


# FLASK-SQLALCHEMY
SQLALCHEMY_DATABASE_URI = \
    'mysql://{username}:{password}@{host}:{port}/{database}'.format(
    username=DB_USERNAME, password=DB_PASSWORD,
    host=DB_HOST, port=DB_PORT,
    database=DB_DATABASE
    )
SQLALCHEMY_POOL_RECYCLE = 10


# FLASK-THEMES
DEFAULT_THEME = 'newstyle'


# FLASK-UPLOADS
UPLOADED_PHOTOS_DEST = 'D:/uploads/photos'
UPLOADED_PHOTOS_URL = 'D:/uploads/photos/'
UPLOADED_PHOTOS_ALLOW = ['jpg', 'jpeg', 'png', 'gif']
UPLOADS_DEFAULT_DEST = 'D:/uploads'
UPLOADS_DEFAULT_URL = 'D:/uploads/'





