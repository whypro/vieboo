# -*- coding: utf-8 -*-
from flask import Module, g, redirect, url_for, flash
from flask.ext.login import login_required
from microblog.forms.friendship import ChatForm
from microblog.models import People, Friendship
from microblog.database import db
from microblog.models.friendship import Chatting
from microblog.tools import render_template


friendship = Module(__name__, url_prefix='/friendship')


@friendship.route('/follow/<int:id>/')
@login_required
def follow(id):
    if g.user.id == id:
        flash(u'不能关注自己', 'error')
    else:
        people = People.query.get(id)
        if g.user.is_following(id):
            flash(u'不能重复关注', 'error')
        elif g.user.is_blocking(id):
            flash(u'不能关注黑名单中的人，请先移出黑名单', 'error')
        elif g.user.is_blocked(id):
            flash(u'对方拒绝了您的关注请求', 'error')
        else:
            g.user.following.append(people)
            db.session.add(g.user)
            db.session.commit()
            flash(u'关注成功', 'success')
    return redirect(url_for('frontend.index'))


@friendship.route('/unfollow/<int:id>/')
@login_required
def unfollow(id):
    people = People.query.get(id)
    if g.user.is_following(id):
        g.user.following.remove(people)
        db.session.add(g.user)
        db.session.commit()
        flash(u'取消成功', 'success')
    return redirect(url_for('frontend.index'))


@friendship.route('/following/')
@login_required
def show_following():
    """查看我关注的人"""
    followings = g.user.following.all()
    return render_template('friendship.html', people=followings)


@friendship.route('/followed/')
@login_required
def show_followed():
    """查看关注我的人"""
    followeds = g.user.followed.all()
    return render_template('friendship.html', people=followeds)


@friendship.route('/block/<int:id>/')
@login_required
def block(id):
    if g.user.id == id:
        flash(u'不能将自己加入黑名单', 'error')
    else:
        people = People.query.get(id)
        if g.user.is_blocking(id):
            flash(u'不能重复加入黑名单', 'error')
        else:
            g.user.blocking.append(people)
            # 取消关注
            if g.user.is_following(id):
                g.user.following.remove(people)
            db.session.add(g.user)
            db.session.commit()
            flash(u'加入黑名单成功', 'success')
    return redirect(url_for('frontend.index'))


@friendship.route('/unblock/<int:id>/')
@login_required
def unblock(id):
    people = People.query.get(id)
    if g.user.is_blocking(id):
        g.user.blocking.remove(people)
        db.session.add(g.user)
        db.session.commit()
        flash(u'取消黑名单成功', 'success')
    return redirect(url_for('frontend.index'))


@friendship.route('/blocking/')
@login_required
def show_blocking():
    """查看黑名单"""
    blockings = g.user.blocking.all()
    return render_template('friendship.html', people=blockings)


@friendship.route('/chat/<int:id>/', methods=['GET', 'POST'])
@login_required
def chat(id):
    chat_form = ChatForm()
    from_people = g.user
    to_people = People.query.get(id)

    if chat_form.validate_on_submit():
        chatting = Chatting(from_people.id, to_people.id, content=chat_form.content.data)
        db.session.add(chatting)
        db.session.commit()
        flash(u'发送成功')
        return redirect(url_for('frontend.index'))

    return render_template(
        'chat.html',
        chat_form=chat_form,
        from_people=from_people,
        to_people=to_people
    )


# TODO:
# dynamic, joined