# -*- coding: utf-8 -*-
from flask import Blueprint, g, flash, redirect, url_for
from flask.ext.login import login_required
from microblog.extensions import db
from microblog.helpers import render_template
from microblog.models import Notification


notification = Blueprint(__name__, url_prefix='/notification')


@notification.route('/')
@login_required
def show_notification():
    notifications = Notification.query.filter_by(to_id=g.user.id).order_by(Notification.create_time.desc()).all()
    return render_template('notification.html', notifications=notifications)


@notification.route('/<int:id>/set-read/')
@login_required
def set_read(id):
    """标记为已读"""
    noti = Notification.query.get_or_404(id)
    if noti.to_id != g.user.id:
        flash(u'权限不足', 'warning')
        return redirect(url_for('notification.show_notification'))
    if not noti.has_read:
        noti.has_read = True
        db.session.add(noti)
        db.session.commit()
    return redirect(url_for('notification.show_notification'))


@notification.route('/<int:id>/set-unread/')
@login_required
def set_unread(id):
    """标记为已读"""
    noti = Notification.query.get_or_404(id)
    if noti.to_id != g.user.id:
        flash(u'权限不足', 'warning')
        return redirect(url_for('notification.show_notification'))
    if noti.has_read:
        noti.has_read = False
        db.session.add(noti)
        db.session.commit()
    return redirect(url_for('notification.show_notification'))


@notification.route('/<int:id>/delete/')
@login_required
def delete_notification(id):
    noti = Notification.query.get_or_404(id)
    if noti.to_id != g.user.id:
        flash(u'权限不足', 'warning')
        return redirect(url_for('notification.show_notification'))
    db.session.delete(noti)
    db.session.commit()
    flash(u'删除成功', 'success')
    return redirect(url_for('notification.show_notification'))
