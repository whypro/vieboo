# -*- coding: utf-8 -*-
from flask import Module, g, url_for, redirect, flash, abort, request
from flask.ext.login import login_required
from microblog.database import db
from microblog.models import Microblog, Comment
from microblog.forms import PostForm, CommentForm
from microblog.tools import render_template

mblog = Module(__name__, url_prefix='/microblog')


# 发布微博
@mblog.route('/post/', methods=['GET', 'POST'])
@login_required
def post():
    post_form = PostForm(request.form)
    print post_form.validate()
    if request.method == 'POST' and post_form.validate():
        microblog = Microblog(g.user.id, post_form.content.data)
        db.session.add(microblog)
        db.session.commit()
        flash(u'发布成功')
        return redirect(url_for('frontend.index'))
    return render_template('post.html', form=post_form)


@mblog.route('/delete/<int:id>/')
@login_required
def delete(id):
    microblog = Microblog.query.get(id)
    if microblog.people_id == g.user.id:
        db.session.delete(microblog)
        db.session.commit()
        flash(u'删除成功')
        # print u'删除成功'
    else:
        flash(u'删除失败')
        # print u'删除失败'
    return redirect(url_for('frontend.index'))


@mblog.route('/comment/<int:mid>/', methods=['GET', 'POST'])
@mblog.route('/comment/<int:mid>/<int:cid>/', methods=['GET', 'POST'])
@login_required
def comment(mid, cid=None):
    microblog = Microblog.query.get(mid)

    if cid:
        parent_comment = Comment.query.get(cid)
        if not parent_comment:
            abort(404)
    else:
        parent_comment = None

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(
            g.user.id,
            comment_form.content.data,
            mid,
            cid
        )
        db.session.add(comment)
        db.session.commit()
        flash(u'评论成功')
        return redirect(url_for('frontend.index'))
    return render_template('comment.html', form=comment_form, microblog=microblog, parent_comment=parent_comment)


