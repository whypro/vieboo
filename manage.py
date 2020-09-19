# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import subprocess
import datetime
import shutil
import os
from zipfile import ZipFile

from flask.ext.script import Manager, Server
from flask.ext.migrate import  MigrateCommand

from microblog import create_app, config
from microblog.extensions import db

current_config = config.LocalDevelopmentConfig

app = create_app(current_config)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
# manager.add_command('debug', Server(host='127.0.0.1', port=8080, debug=True))


@manager.command
def debug():
    """Start Server in debug mode"""
    app.run(host='0.0.0.0', port=5000, debug=True, processes=3)


@manager.command
def init():
    # 创建数据库
    create_db_sql = 'CREATE DATABASE IF NOT EXISTS {0} DEFAULT CHARACTER SET utf8'.format(current_config.DB_DATABASE)
    # print create_db_sql
    ret = subprocess.call(
        [
            'mysql',
            '-h', current_config.DB_HOST,
            '-P', str(current_config.DB_PORT),
            '-u', current_config.DB_USERNAME,
            '-p{0}'.format(current_config.DB_PASSWORD),
            '-e', create_db_sql,
        ]
    )
    if not ret:
        print '数据库创建成功'
    else:
        print '数据库创建失败'
        return 

    db.drop_all()
    db.create_all()
    print '数据表创建成功'
    # 数据初始化代码
    # print '数据初始化成功'


@manager.command
def backup():
    # 备份上传文件
    date_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    ret = shutil.make_archive('backup/uploads-{date}'.format(date=date_str), 'zip', './', 'uploads')
    print '文件已备份至 {0}'.format(ret)
    # print ret

    # 备份数据库
    sql_file = 'backup/microblog-{date}.sql'.format(date=date_str)
    f = open(sql_file, 'w')
    ret = subprocess.call(
        [
            'mysqldump',
            '-h', current_config.DB_HOST,
            '-P', str(current_config.DB_PORT),
            '-u', current_config.DB_USERNAME,
            '-p{0}'.format(current_config.DB_PASSWORD),
            current_config.DB_DATABASE,
        ],
        stdout=f
    )
    f.close()
    if not ret:
        print '数据库已备份至 {0}'.format(os.path.abspath(sql_file))
    else:
        os.remove(sql_file)
        print '数据库备份失败'


@manager.command
def restore():
    files = os.listdir('backup')
    print '可以还原的备份文件有：'
    print '\n'.join(set([bf.split('-')[-1].split('.')[0] for bf in files]))
    print '请选择备份文件日期：'
    date_str = raw_input()

    # 还原数据库
    f = open('backup/microblog-{date}.sql'.format(date=date_str), 'r')
    ret = subprocess.call(
        [
            'mysql',
            '-h', current_config.DB_HOST,
            '-P', str(current_config.DB_PORT),
            '-u', current_config.DB_USERNAME,
            '-p{0}'.format(current_config.DB_PASSWORD),
            current_config.DB_DATABASE,
        ],
        stdin=f
    )
    f.close()
    if not ret:
        print '数据库已还原'
    else:
        print '数据库还原失败'

    # 还原上传文件
    with ZipFile('backup/uploads-{date}.zip'.format(date=date_str), 'r') as z:
        z.extractall()
    print '文件已还原'


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, processes=10, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
    manager.run()
