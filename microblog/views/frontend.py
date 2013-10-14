# -*- coding: utf-8 -*-
import datetime
from flask import Module, g, request, url_for, redirect, flash
from flask.ext.login import login_user, login_required, logout_user
from microblog.database import db
from microblog.forms.accounts import ModifyProfileForm
from microblog.models import People
from microblog.forms import LoginForm, RegisterForm, ChangePasswordForm
from microblog.tools import render_template

frontend = Module(__name__)


@frontend.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# 用户注册
@frontend.route('/register/', methods=['GET', 'POST'])
def register():
    # 已登录用户则返回首页
    if g.user.is_authenticated():
        return redirect(url_for('index'))

    register_form = RegisterForm()
    if register_form.validate_on_submit():
        # 获取 ip 地址
        if 'x-forwarded-for' in request.headers:
            ip = request.headers['x-forwarded-for'].split(', ')[0]
        else:
            ip = request.remote_addr
        people = People(
            email=register_form.email.data,
            password=register_form.password.data,
            nickname=register_form.nickname.data,
            mobile=register_form.mobile.data,
            reg_time=datetime.datetime.utcnow(),
            reg_ip=ip,
        )
        # 将用户写入数据库
        db.session.add(people)
        db.session.commit()
        flash(u'注册成功')
        return redirect(url_for('index'))
    return render_template('register.html', form=register_form)


@frontend.route('/login/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        people = People.query.authenticate(
            login_form.login.data,
            login_form.password.data,
        )

        if people:
            login_user(people, remember=login_form.remember.data)
            flash(u'登录成功')
            return redirect(url_for('index'))
        else:
            flash(u'登录失败')

    return render_template('login.html', form=login_form)


# 修改密码
@frontend.route('/password/', methods=['GET', 'POST'])
@login_required
def password():
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        people = People.query.authenticate(
            g.user.get_email(),
            change_password_form.password_old.data,
        )
        if people:
            people.change_password(change_password_form.password_new.data)
            db.session.add(people)
            db.commit()
            flash(u'密码修改成功')
            return redirect(url_for('index'))
        else:
            flash(u'原密码不正确')
            return redirect(url_for('password'))

    return render_template('password.html', form=change_password_form)


# 注销
@frontend.route('/logout/')
@login_required
def logout():
    logout_user()
    flash(u'已注销')
    return redirect(url_for('index'))


@frontend.route('/install/')
def install():
    db.create_all()
    flash(u'创建成功')
    return redirect(url_for('index'))

# 显示与修改个人资料
@frontend.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    people = g.user
    profile_form = ModifyProfileForm(obj=people)
    if profile_form.validate_on_submit():
        new_password = profile_form.password.data
        new_nickname = profile_form.nickname.data
        new_mobile = profile_form.mobile.data
        if new_password:
            people.change_password(new_password)
        if new_nickname:
            people.change_nickname(new_nickname)
        if new_mobile:
            people.change_mobile(new_mobile)
        db.session.add(people)
        db.session.commit()
        flash(u'个人资料修改成功')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=profile_form)