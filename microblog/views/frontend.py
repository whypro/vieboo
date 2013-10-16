# -*- coding: utf-8 -*-
import datetime
from flask import Module, g, request, url_for, redirect, flash
from flask.ext.login import login_user, login_required, logout_user
from microblog.database import db
from microblog.forms.account import ModifyProfileForm
from microblog.models import People, Microblog
from microblog.forms import LoginForm, RegisterForm, ChangePasswordForm, PostForm
from microblog.tools import render_template

frontend = Module(__name__)


@frontend.route('/')
def index():
    microblogs = Microblog.query.order_by(Microblog.post_time.desc()).limit(10).all()
    #print microblogs
    return render_template('index.html', microblogs=microblogs)


@frontend.route('/install/')
def install():
    db.create_all()
    flash(u'创建成功')
    return redirect(url_for('index'))


@frontend.route('/people/<int:id>/')
def people(id):
    people = People.query.get(id)
    return render_template('people.html', people=people)