# -*- coding: utf-8 -*-
from flask import Module, g, redirect, url_for, flash
from microblog.models import People, Friendship
from microblog.database import db

friendship = Module(__name__, url_prefix='/friendship')


@friendship.route('/follow/<int:id>/')
def follow(id):
    if g.user.id == id:
        flash(u'不能关注自己')
    else:
        people = People.query.get(id)
        if g.user.is_following(id):
            flash(u'不能重复关注')
        else:
            g.user.following.append(people)
            db.session.add(g.user)
            db.session.commit()
            flash(u'关注成功')
    return redirect(url_for('frontend.index'))


@friendship.route('/unfollow/<int:id>/')
def unfollow(id):
    people = People.query.get(id)
    if g.user.is_following(id):
        g.user.following.remove(people)
        db.session.add(g.user)
        db.session.commit()
        flash(u'取消成功')
    return redirect(url_for('frontend.index'))


@friendship.route('/block/<int:id>/')
def block(id):
    if g.user.id == id:
        flash(u'不能将自己加入黑名单')
    else:
        people = People.query.get(id)
        if g.user.is_blocking(id):
            flash(u'不能重复加入黑名单')
        else:
            g.user.blocking.append(people)
            # 取消关注
            if g.user.is_following(id):
                g.user.following.remove(people)
            db.session.add(g.user)
            db.session.commit()
            flash(u'加入黑名单成功')
    return redirect(url_for('frontend.index'))


@friendship.route('/unblock/<int:id>/')
def unblock(id):
    people = People.query.get(id)
    if g.user.is_blocking(id):
        g.user.blocking.remove(people)
        db.session.add(g.user)
        db.session.commit()
        flash(u'取消黑名单成功')
    return redirect(url_for('frontend.index'))


@friendship.route('/chat/')
def chat():
    return u'未完成'


# TODO:
# dynamic, joined