# -*- coding: utf-8 -*-

from flask import Module, redirect, url_for, flash
from flask.ext.login import login_required
from microblog.extensions import db
from microblog.models import People, Microblog, LoginLog, VisitLog
from microblog.helpers import render_template
from microblog.permission import admin as admin_permission

admin = Module(__name__, url_prefix='/admin')


@admin.route('/')
@login_required
@admin_permission.require(401)
def index():
    return render_template('admin/index.html')


@admin.route('/people/', defaults={'page': 1})
@admin.route('/people/page/<int:page>/')
@login_required
@admin_permission.require(401)
def show_people(page):
    pagination = People.query.paginate(page, per_page=50)
    people = pagination.items
    return render_template(
        'admin/people.html',
        people=people,
        pagination=pagination
    )


@admin.route('/people/block/<int:id>/')
@login_required
@admin_permission.require(401)
def block_people(id):
    people = People.query.get_or_404(id)
    if people.status != 'blocked':
        people.status = 'blocked'
        db.session.add(people)
        db.session.commit()
        flash(u'禁言成功', 'success')
    return redirect(url_for('show_people'))


@admin.route('/people/unblock/<int:id>/')
@login_required
@admin_permission.require(401)
def unblock_people(id):
    people = People.query.get_or_404(id)
    if people.status != 'active':
        people.status = 'active'
        db.session.add(people)
        db.session.commit()
        flash(u'取消禁言成功', 'success')
    return redirect(url_for('show_people'))


@admin.route('/people/delete/<int:id>/')
@login_required
@admin_permission.require(401)
def delete_people(id):
    people = People.query.get_or_404(id)
    people.status = 'deleted'
    db.session.add(people)
    db.session.commit()
    flash(u'用户已删除', 'success')
    return redirect(url_for('show_people'))


@admin.route('/microblog/', defaults={'page': 1})
@admin.route('/microblog/page/<int:page>/')
@login_required
@admin_permission.require(401)
def show_microblog(page):
    pagination = Microblog.query.order_by(Microblog.post_time.desc()).\
        paginate(page, per_page=50)
    microblogs = pagination.items
    return render_template(
        'admin/microblog.html',
        microblogs=microblogs,
        pagination=pagination
    )


@admin.route('/microblog/delete/<int:id>/')
@login_required
@admin_permission.require(401)
def delete_microblog(id):
    microblog = Microblog.query.get_or_404(id)
    db.session.delete(microblog)
    db.session.commit()
    flash(u'微博已删除', 'success')
    return redirect(url_for('show_microblog'))


@admin.route('/login-log/', defaults={'page': 1})
@admin.route('/login-log/page/<int:page>/')
@login_required
@admin_permission.require(401)
def show_login_log(page):
    pagination = LoginLog.query.order_by(LoginLog.login_time.desc()).\
        paginate(page, per_page=50)
    login_logs = pagination.items
    return render_template(
        'admin/login-log.html',
        login_logs=login_logs,
        pagination=pagination
    )


@admin.route('/visit-log/', defaults={'page': 1})
@admin.route('/visit-log/page/<int:page>/')
@login_required
@admin_permission.require(401)
def show_visit_log(page):
    pagination = VisitLog.query.order_by(VisitLog.visit_time.desc()).\
        paginate(page, per_page=50)
    # For BAE fucking MySQL
    # pagination = VisitLog.query.paginate(page, per_page=50)
    visit_logs = pagination.items
    return render_template(
        'admin/visit-log.html',
        visit_logs=visit_logs,
        pagination=pagination
    )


@admin.route('/visit-log/<int:id>/delete/')
@login_required
@admin_permission.require(401)
def delete_visit_log(id):
    visit_log = VisitLog.query.get(id)
    db.session.delete(visit_log)
    db.session.commit()
    return redirect(url_for('show_visit_log'))


@admin.route('/install/')
def install():
    db.create_all()
    flash(u'数据库初始化成功', 'success')
    return redirect(url_for('index'))
