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
        if g.user.has_following(id):
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
    if g.user.has_following(id):
        g.user.following.remove(people)
        db.session.add(g.user)
        db.session.commit()
        flash(u'取消成功')
    return redirect(url_for('frontend.index'))

# TODO:
# dynamic, joined