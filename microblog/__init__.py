# -*- coding: utf-8 -*-
import datetime
from sqlalchemy.exc import ProgrammingError

from flask import Flask, g, flash, redirect, url_for, request
from flask.ext.login import LoginManager, current_user
from flask.ext.themes import setup_themes
from flask.ext.uploads import configure_uploads, patch_request_class
from flask_wtf import CsrfProtect
from flask.ext.principal import Principal, identity_loaded, RoleNeed, UserNeed, identity_changed
from flask.ext.gemoji import Gemoji
from microblog import views
from microblog.extensions import db
from microblog.models import People, VisitLog
from microblog.helpers import get_client_ip


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    Gemoji.init_app(app)

    configure_modules(app)
    config_error_handlers(app)
    configure_theme(app)
    configure_flasklogin(app)
    config_before_request(app)
    # configure_uploads(app, (photos, ))
    patch_request_class(app)    # 16M limit

    CsrfProtect(app)
    configure_identity(app)

    return app


def configure_modules(app):
    app.register_blueprint(views.frontend)
    app.register_blueprint(views.account)
    app.register_blueprint(views.mblog)
    app.register_blueprint(views.friendship)
    app.register_blueprint(views.admin)
    app.register_blueprint(views.oauth2)
    app.register_blueprint(views.photo)
    app.register_blueprint(views.notification)


def configure_theme(app):
    setup_themes(app)


def configure_flasklogin(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(_id):
        try:
            people = People.query.get(_id)
        except:
            people = None
        return people

    @login_manager.unauthorized_handler
    def unauthorized():
        flash(u'请先登录', 'warning')
        return redirect(url_for('account.login'))


def config_before_request(app):
    @app.before_request
    def before_request():
        g.user = current_user

        if g.user.is_authenticated() and g.user.is_admin():
            # TODO: 管理员不记录行为，？
            pass
        else:
            url = request.url
            method = request.method
            user_agent = request.user_agent
            referrer = request.referrer
            platform = user_agent.platform
            browser = user_agent.browser
            version = user_agent.version
            client_ip = get_client_ip()
            visit_time = datetime.datetime.now()
            people_id = getattr(g.user, 'id', None)
            # 忽略静态文件的访问
            if str(url)[-1] != '/':
                pass
            else:
                visit_log = VisitLog(
                    url, method, referrer,
                    platform, browser, version,
                    client_ip, visit_time, people_id
                )
                db.session.add(visit_log)
                try:
                    db.session.commit()
                except ProgrammingError:
                    print 'never mind.'


def config_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        flash(u'页面未找到', 'danger')
        return redirect(url_for('frontend.index'))

    @app.errorhandler(401)
    def unauthorized(e):
        flash(u'未经授权', 'danger')
        return redirect(url_for('frontend.index'))

    @app.errorhandler(500)
    def internal_server_error(e):
        flash(u'服务器开小差了', 'danger')
        return redirect(url_for('frontend.index'))


def configure_identity(app):
    principal = Principal(app)

    @identity_loaded.connect_via(app)
    # @identity_changed.connect_via(app)
    def on_identity_loaded(sender, identity):
        print 'received from', str(sender)
        identity.user = g.user
        if hasattr(g.user, 'id'):
            identity.provides.add(UserNeed(g.user.id))
        if hasattr(g.user, 'roles'):
            for role in g.user.roles:
                print role.name
                identity.provides.add(RoleNeed(role.name))


