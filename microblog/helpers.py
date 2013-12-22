# -*- coding: utf-8 -*-
import os
from urlparse import urlparse, urljoin
from flask import current_app, request, url_for, redirect
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


# redirect back
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        elif is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)
# redirect back