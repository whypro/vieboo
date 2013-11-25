# -*- coding: utf-8 -*-

from flask import Module, g, redirect, url_for, request, flash
from microblog.extensions import db
from microblog.models import People, Microblog, LoginLog
from microblog.helpers import render_template

admin = Module(__name__, url_prefix='/admin')


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/people/')
def show_people():
    people = People.query.all()
    return render_template('admin/people.html', people=people)


@admin.route('/people/block/<int:id>/')
def block_people(id):
    people = People.query.get_or_404(id)
    people.status = 'blocked'
    db.session.add(people)
    db.session.commit()
    flash(u'已禁言', 'success')
    return redirect(url_for('show_people'))


@admin.route('/people/unblock/<int:id>/')
def unblock_people(id):
    people = People.query.get_or_404(id)
    people.status = 'active'
    db.session.add(people)
    db.session.commit()
    flash(u'已取消禁言', 'success')
    return redirect(url_for('show_people'))


@admin.route('/people/delete/<int:id>/')
def delete_people(id):
    people = People.query.get_or_404(id)
    people.status = 'deleted'
    db.session.add(people)
    db.session.commit()
    flash(u'用户已删除', 'success')
    return redirect(url_for('show_people'))


@admin.route('/microblog/')
def show_microblog():
    microblogs = Microblog.query.all()
    return render_template('admin/microblog.html', microblogs=microblogs)


@admin.route('/microblog/delete/<int:id>/')
def delete_microblog(id):
    microblog = Microblog.query.get_or_404(id)
    db.session.delete(microblog)
    db.session.commit()
    flash(u'微博已删除', 'success')
    return redirect(url_for('show_microblog'))


@admin.route('/login-log/')
def show_login_log():
    login_logs = LoginLog.query.all()
    return render_template('admin/login-log.html', login_logs=login_logs)


@admin.route('/install/')
def install():
    db.create_all()
    flash(u'数据库初始化成功', 'success')
    return redirect(url_for('index'))
