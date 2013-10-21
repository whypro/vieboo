# -*- coding: utf-8 -*-
import os
import sys
# 将依赖模块文件夹加入系统路径
deps_path = os.path.join(os.path.split(os.path.realpath(__file__))[0],'deps')
sys.path.insert(0, deps_path)

from flask import Flask, g
from flask.ext.login import LoginManager, current_user
from flask.ext.themes import setup_themes
from microblog import views
from microblog.database import db
from microblog.models import People


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    configure_modules(app)
    configure_theme(app)
    configure_flasklogin(app)
    config_before_request(app)

    return app


def configure_modules(app):
    app.register_module(views.frontend)
    app.register_module(views.account)
    app.register_module(views.mblog)
    app.register_module(views.friendship)


def configure_theme(app):
    setup_themes(app)


def configure_flasklogin(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(_id):
        return People.query.get(_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        return '请先登录'


def config_before_request(app):
    @app.before_request
    def before_request():
        g.user = current_user