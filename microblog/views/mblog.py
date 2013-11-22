# -*- coding: utf-8 -*-
from flask import Module, g, url_for, redirect, flash, abort, request
from flask.ext.login import login_required
from microblog.extensions import db
from microblog.models import Microblog, Comment
from microblog.forms import PostForm, CommentForm, RepostForm
from microblog.helpers import render_template

mblog = Module(__name__, url_prefix='/microblog')


# 发布微博
@mblog.route('/post/', methods=['GET', 'POST'])
@login_required
def post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        microblog = Microblog(g.user.id, post_form.content.data)
        db.session.add(microblog)
        db.session.commit()
        flash(u'发布成功', 'success')
        return redirect(url_for('frontend.index'))
    return render_template('post.html', form=post_form)


@mblog.route('/delete/<int:id>/')
@login_required
def delete(id):
    microblog = Microblog.query.get(id)
    if microblog.people_id == g.user.id:
        db.session.delete(microblog)
        db.session.commit()
        flash(u'删除成功', 'success')
        # print u'删除成功'
    else:
        flash(u'删除失败', 'warning')
        # print u'删除失败'
    return redirect(url_for('frontend.index'))


@mblog.route('/comment/<int:mid>/', methods=['GET', 'POST'])
@mblog.route('/comment/<int:mid>/<int:cid>/', methods=['GET', 'POST'])
@login_required
def comment(mid, cid=None):
    microblog = Microblog.query.get(mid)

    # 如果是对评论的评论，则在表单中显示回复的目标（字符串）
    # 并在提交时使用切片运算忽略该字符串
    if cid:
        parent_comment = Comment.query.get(cid)
        if not parent_comment:
            abort(404)
        # 不能回复自己
        if g.user.id == parent_comment.people.id:
            flash(u'不能回复自己', 'warning')
            return redirect(url_for('mblog.comment', mid=mid))
        content = u'回复 ' + parent_comment.people.nickname + ': '
    else:
        parent_comment = None
        content = ''
    comment_form = CommentForm(content=content)
    if comment_form.validate_on_submit():
        comment = Comment(
            g.user.id,
            comment_form.content.data[len(content):],
            mid,
            cid
        )
        db.session.add(comment)
        db.session.commit()
        flash(u'评论成功', 'success')
        return redirect(url_for('mblog.comment', mid=mid))
    return render_template('comment.html', form=comment_form, microblog=microblog, parent_comment=parent_comment)


@mblog.route('/comment/delete/<int:id>/')
@login_required
def delete_comment(id):
    comment = Comment.query.get(id)
    mid = comment.microblog_id
    if comment.people_id == g.user.id:
        db.session.delete(comment)
        db.session.commit()
        flash(u'删除成功', 'success')
        # print u'删除成功'
    else:
        flash(u'删除失败', 'warning')
        # print u'删除失败'
    return redirect(url_for('mblog.comment', mid=mid))


@mblog.route('/repost/<int:id>/', methods=['GET', 'POST'])
@login_required
def repost(id):
    microblog = Microblog.query.get(id)
    repost_form = RepostForm()
    if repost_form.validate_on_submit():
        rp_microblog = Microblog(g.user.id, repost_form.content.data, parent_microblog_id=id)
        db.session.add(rp_microblog)
        db.session.commit()
        flash(u'转发成功', 'success')
        return redirect(url_for('frontend.index'))
    return render_template('repost.html', form=repost_form, microblog=microblog)