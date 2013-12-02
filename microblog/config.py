# -*- coding:utf-8 -*-
import os

if 'SERVER_SOFTWARE' in os.environ:
    # 生产服务器配置
    from bae.core import const
    # 数据库配置
    DB_HOST = const.MYSQL_HOST
    DB_DATABASE = 'ersVIiuGQNlnwijllSmh'
    DB_USERNAME = const.MYSQL_USER
    DB_PASSWORD = const.MYSQL_PASS
    DB_PORT = int(const.MYSQL_PORT)

else:
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
SQLALCHEMY_POOL_RECYCLE = 10

# FLASK-THEMES
DEFAULT_THEME = 'newstyle'

# FLASK-UPLOADS
UPLOADED_PHOTOS_DEST = 'D:/uploads/photos'
UPLOADED_PHOTOS_URL = 'D:/uploads/photos/'
UPLOADED_PHOTOS_ALLOW = ['jpg', 'jpeg', 'png', 'gif']
UPLOADS_DEFAULT_DEST = 'D:/uploads'
UPLOADS_DEFAULT_URL = 'D:/uploads/'

DEBUG = True
SECRET_KEY = 'hello world'

PER_PAGE = 5
