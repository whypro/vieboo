# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, g, url_for, redirect, flash, abort, request
from flask.ext.login import login_required
from microblog.extensions import db
from microblog.models import Microblog, Comment
from microblog.forms import PostForm, CommentForm, RepostForm
from microblog.helpers import render_template
from microblog.models.notification import Notification

mblog = Blueprint('mblog', __name__, url_prefix='/microblog')


# 发布微博
@mblog.route('/post/', methods=['GET', 'POST'])
@login_required
def post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        microblog = Microblog(g.user.id, post_form.content.data)
        db.session.add(microblog)
        db.session.commit()
        flash('发布成功', 'success')
        return redirect(url_for('frontend.index'))
    return render_template('post.html', form=post_form)


@mblog.route('/<int:id>/delete/')
@login_required
def delete(id):
    microblog = Microblog.query.get_or_404(id)
    if microblog.people_id == g.user.id:
        db.session.delete(microblog)
        db.session.commit()
        flash('删除成功', 'success')
        # print '删除成功'
    else:
        flash('删除失败', 'warning')
        # print '删除失败'
    return redirect(url_for('frontend.index'))


@mblog.route('/<int:mid>/comment/', methods=['GET', 'POST'])
@mblog.route('/<int:mid>/comment/<int:cid>/', methods=['GET', 'POST'])
@login_required
def comment(mid, cid=None):
    microblog = Microblog.query.get_or_404(mid)

    # 如果是对评论的评论，则在表单中显示回复的目标（字符串）
    # 并在提交时使用切片运算忽略该字符串
    if cid:
        parent_comment = Comment.query.get_or_404(cid)
        # 不能回复自己
        if g.user.id == parent_comment.people.id:
            flash('不能回复自己', 'warning')
            return redirect(url_for('mblog.comment', mid=mid))
        content = '回复 ' + parent_comment.people.nickname + ': '
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
        if cid and g.user.id != parent_comment.people_id:
            notification = Notification(
                from_id=g.user.id, to_id=parent_comment.people_id,
                object_table='comment', object_id=comment.id
            )
            db.session.add(notification)
            db.session.commit()
        elif g.user.id != microblog.people_id:
            notification = Notification(
                from_id=g.user.id, to_id=microblog.people_id,
                object_table='microblog', object_id=mid
            )
            db.session.add(notification)
            db.session.commit()
        flash('评论成功', 'success')
        return redirect(url_for('mblog.comment', mid=mid))
    return render_template(
        'comment.html',
        form=comment_form,
        microblog=microblog,
        parent_comment=parent_comment
    )


@mblog.route('/comment/<int:id>/delete/')
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    mid = comment.microblog_id
    if comment.people_id == g.user.id:
        db.session.delete(comment)
        db.session.commit()
        flash('删除成功', 'success')
        # print '删除成功'
    else:
        flash('删除失败', 'warning')
        # print '删除失败'
    return redirect(url_for('mblog.comment', mid=mid))


@mblog.route('/<int:id>/repost/', methods=['GET', 'POST'])
@login_required
def repost(id):
    microblog = Microblog.query.get_or_404(id)
    repost_form = RepostForm()
    if repost_form.validate_on_submit():
        rp_microblog = Microblog(g.user.id, repost_form.content.data, parent_microblog_id=id)
        db.session.add(rp_microblog)
        if g.user.id != microblog.people_id:
            notification = Notification(
                from_id=g.user.id, to_id=microblog.people_id,
                object_table='microblog', object_id=id
            )
            db.session.add(notification)
        db.session.commit()
        flash('转发成功', 'success')
        return redirect(url_for('frontend.index'))
    return render_template('repost.html', form=repost_form, microblog=microblog)