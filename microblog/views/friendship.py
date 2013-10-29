# -*- coding: utf-8 -*-
from flask import Module, g, redirect, url_for, flash
from microblog.forms.friendship import ChatForm
from microblog.models import People, Friendship
from microblog.database import db
from microblog.models.friendship import Chatting
from microblog.tools import render_template

friendship = Module(__name__, url_prefix='/friendship')


@friendship.route('/follow/<int:id>/')
def follow(id):
    if g.user.id == id:
        flash(u'不能关注自己', 'error')
    else:
        people = People.query.get(id)
        if g.user.is_following(id):
            flash(u'不能重复关注', 'error')
        else:
            g.user.following.append(people)
            db.session.add(g.user)
            db.session.commit()
            flash(u'关注成功', 'success')
    return redirect(url_for('frontend.index'))


@friendship.route('/unfollow/<int:id>/')
def unfollow(id):
    people = People.query.get(id)
    if g.user.is_following(id):
        g.user.following.remove(people)
        db.session.add(g.user)
        db.session.commit()
        flash(u'取消成功', 'success')
    return redirect(url_for('frontend.index'))


@friendship.route('/following/')
def show_following():
    followings = g.user.followed.all()
    return '未完成'
    # return render_template('index.html', people=followings)


@friendship.route('/followed/')
def show_followed():
    pass


@friendship.route('/block/<int:id>/')
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
def unblock(id):
    people = People.query.get(id)
    if g.user.is_blocking(id):
        g.user.blocking.remove(people)
        db.session.add(g.user)
        db.session.commit()
        flash(u'取消黑名单成功', 'success')
    return redirect(url_for('frontend.index'))


@friendship.route('/blocking/')
def show_blocking():
    pass


@friendship.route('/chat/<int:id>/', methods=['GET', 'POST'])
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