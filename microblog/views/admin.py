# -*- coding: utf-8 -*-
from flask import Module, g, redirect, url_for, request, flash
from flask.ext.login import login_user
from microblog.database import db
from microblog.forms import LoginForm
from microblog.models import People, LoginLog, Microblog
from microblog.tools import render_template
from microblog.views.account import get_client_ip

admin = Module(__name__, url_prefix='/admin')


@admin.route('/')
def index():
    return 'hello'


@admin.route('/people/')
def show_people():
    people = People.query.all()
    return render_template('admin/people.html', people=people)


@admin.route('/microblog/')
def show_microblog():
    microblogs = Microblog.query.all()
    return render_template('admin/microblog.html', microblogs=microblogs)