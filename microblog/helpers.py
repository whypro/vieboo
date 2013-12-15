# -*- coding: utf-8 -*-
import os
from flask import current_app, request, url_for
from flask.ext.themes import render_theme_template



def get_default_theme():
    return current_app.config['DEFAULT_THEME']


def render_template(template, **context):
    return render_theme_template(get_default_theme(), template, **context)


def get_client_ip():
    # 获取 ip 地址
    if 'x-forwarded-for' in request.headers:
        ip = request.headers['x-forwarded-for'].split(', ')[0]
    else:
        ip = request.remote_addr
    return ip


def render_uri(uri):
    #if uri.startswith('http'):
    #    return url_for('frontend.remote_photo') + '?uri=' + uri
    #else:
    return url_for('frontend.uploads', filename=uri)


def get_uploader():
    if not current_app.config['USE_BCS_BUCKET']:
        from microblog.uploader import LocalUploader
        uploader = LocalUploader()
    elif 'SERVER_SOFTWARE' in os.environ:
        from microblog.uploader import BCSAPIUploader
        uploader = BCSAPIUploader()
    else:
        from microblog.uploader import BCSSDKUploader
        uploader = BCSSDKUploader()
    return uploader