# -*- coding: utf-8 -*-
import datetime
from flask import Module, g, request, url_for, redirect, flash
from flask.ext.login import login_user, login_required, logout_user
from microblog.database import db
from microblog.forms.account import ModifyProfileForm
from microblog.models import People, Microblog
from microblog.forms import LoginForm, RegisterForm, ChangePasswordForm, PostForm
from microblog.tools import render_template

mblog = Module(__name__, url_prefix='/microblog')

# 发布微博
@mblog.route('/post/', methods=['GET', 'POST'])
@login_required
def post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        microblog = Microblog(g.user.get_id(), post_form.content.data)
        db.session.add(microblog)
        db.session.commit()
        flash(u'发布成功')
        return redirect(url_for('frontend.index'))
    return render_template('post.html', form=post_form)


@mblog.route('/delete/<int:id>/')
@login_required
def delete(id):
    microblog = Microblog.query.get(id)
    if unicode(microblog.people_id) == g.user.get_id():
        db.session.delete(microblog)
        db.session.commit()
        flash(u'删除成功')
        print u'删除成功'
    else:
        flash(u'删除失败')
        print u'删除失败'
    return redirect(url_for('frontend.index'))