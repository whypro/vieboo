# -*- coding: utf-8 -*-
from microblog.extensions import db
import datetime
from microblog.models.account import People


class Microblog(db.Model):
    __tablename__ = 'microblog'

    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(
        db.Integer,
        db.ForeignKey(People.id, ondelete='CASCADE'),
        nullable=False
    )
    parent_microblog_id = db.Column(db.Integer, db.ForeignKey('microblog.id', ondelete='CASCADE'))
    content = db.Column(db.Text, nullable=False)
    post_time = db.Column(db.DateTime, default=datetime.datetime.now)
    comments = db.relationship(
        'Comment', backref='microblog', lazy='dynamic',
        passive_deletes=True)

    def __init__(self, people_id, content, parent_microblog_id=None):
        self.people_id = people_id

        if parent_microblog_id:
            self.parent_microblog_id = parent_microblog_id
            parent_microblog = Microblog.query.get(parent_microblog_id)
            self.content = content + ' //' + parent_microblog.people.nickname + ': ' + parent_microblog.content
        else:
            self.content = content


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(
        db.Integer,
        db.ForeignKey(People.id, ondelete='CASCADE'),
        nullable=False
    )
    microblog_id = db.Column(
        db.Integer,
        db.ForeignKey(Microblog.id, ondelete='CASCADE'),
        nullable=False
    )
    parent_comment_id = db.Column(
        db.Integer,
        db.ForeignKey('comment.id', ondelete='CASCADE'),
    )
    content = db.Column(db.Text, nullable=False)
    comment_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, people_id, content, microblog_id, parent_commnet_id=None):
        self.people_id = people_id
        self.content = content
        self.microblog_id = microblog_id
        self.parent_comment_id = parent_commnet_id