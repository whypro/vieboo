# -*- coding: utf-8 -*-

from flask import Module, g, redirect, url_for, request, flash
from microblog.extensions import db
from microblog.models import People, Microblog
from microblog.tools import render_template

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


@admin.route('/install/')
def install():
    db.create_all()
    flash(u'创建成功', 'success')
    return redirect(url_for('index'))
