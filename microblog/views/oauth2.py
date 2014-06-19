# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, g, current_app, flash, url_for
# from douban_client import DoubanClient
# from douban_client.api.error import DoubanAPIError
from flask.ext.login import login_user
from flask.ext.principal import identity_changed
from microblog.helpers import get_client_ip
from microblog.models import People, LoginLog


oauth2 = Blueprint(__name__, url_prefix='/oauth2')

# KEY = '057e043485cf074a107a0c9d916d15de'
# SECRET = 'a0d5b7822e03f8b2'
# CALLBACK = 'http://localhost:5000/oauth2/douban/'
# SCOPE = 'douban_basic_common,community_basic_user'

# client = DoubanClient(KEY, SECRET, CALLBACK, SCOPE)


@oauth2.route('/sinaweibo/')
def sinaweibo_callback():
    code = request.args.get('code')
    flash(u'您的授权码是：{0}'.format(code), 'info')
    return redirect(url_for('frontend.index'))


# @oauth2.route('/douban/<sitename>/')
# def index(sitename):


#     code = request.args.get('code', None)
#     client.auth_with_code(code)

#     try:
#         me = client.user.me
#         nickname = me.get('name', None)
#         avatar = me.get('large_avatar', None)
#     except DoubanAPIError as e:
#         return str(e.msg)
#     people = People('whypro@live', '123')
#     people.nickname = nickname
#     people.avatar = avatar
#     login_user(people)
#     ip = get_client_ip()
#     login_log = LoginLog(people.id, ip)


#     flash(u'登录成功', 'success')
#     return redirect(url_for('frontend.index'))


# @oauth2.route('/login/')
# def login():
#     return redirect(client.authorize_url)
