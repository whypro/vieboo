# -*- coding: utf-8 -*-
import datetime
from flask import url_for
from markupsafe import Markup
from microblog.models import People, Microblog, Comment, PhotoAlbum, Photo
from microblog.extensions import db


class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='SET NULL'))
    to_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='CASCADE'))
    object_table = db.Column(db.String(20))
    object_id = db.Column(db.Integer)
    content = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    has_read = db.Column(db.Boolean, default=False)

    from_people = db.relationship('People', primaryjoin=(from_id==People.id))
    to_people = db.relationship(
        'People',
        primaryjoin=(to_id==People.id),
        backref=db.backref('notifications', lazy='dynamic'),
        passive_deletes=True
    )

    def __repr__(self):
        if self.object_table == 'microblog':
            obj = Microblog.query.get(self.object_id)
            pattern = u'<a href="%s">%s</a> 在微博 <a href="%s">%s</a> 中回复了你'
            return pattern % (
                url_for('frontend.people', id=self.from_id), Markup.escape(self.from_people.nickname),
                url_for('mblog.comment', mid=self.object_id) if obj else '', Markup.escape(obj.content[:20]) if obj else u'抱歉，该微博已删除'
            )
        elif self.object_table == 'comment':
            obj = Comment.query.get(self.object_id)
            pattern = u'<a href="%s">%s</a> 在评论 <a href="%s">%s</a> 中回复了你'
            return pattern % (
                url_for('frontend.people', id=self.from_id), Markup.escape(self.from_people.nickname),
                url_for('mblog.comment', mid=obj.microblog_id, cid=self.object_id) if obj else '', Markup.escape(obj.parent_comment.content[:20]) if obj else u'抱歉，该评论已删除'
            )
        elif self.object_table == 'photo':
            obj = Photo.query.get(self.object_id)
            pattern = u'<a href="%s">%s</a> 在照片 <a href="%s">%s</a> 中回复了你'
            return pattern % (
                url_for('frontend.people', id=self.from_id), Markup.escape(self.from_people.nickname),
                url_for('photo.show_photo', pid=obj.id, aid=self.album_id) if obj else '', Markup.escape(obj.title[:20]) if obj else u'抱歉，该照片已删除'
            )
        elif self.object_table == 'album':
            obj = PhotoAlbum.query.get(self.object_id)
            pattern = u'<a href="%s">%s</a> 在相册 <a href="%s">%s</a> 中回复了你'
            return pattern % (
                url_for('frontend.people', id=self.from_id), Markup.escape(self.from_people.nickname),
                url_for('photo.show_album', id=obj.id) if obj else '', Markup.escape(obj.title[:20]) if obj else u'抱歉，该相册已删除'
            )
        elif self.object_table == 'chatting':
            pattern = u'<a href="%s">%s</a> 给你发来了一条 <a href="%s">私信</a>'
            return pattern % (
                url_for('frontend.people', id=self.from_id), Markup.escape(self.from_people.nickname),
                url_for('friendship.show_chatting_detail', box='inbox', id=self.object_id)
            )
        elif self.object_table == 'friendship':
            pattern = u'<a href="%s">%s</a> 关注了你'
            return pattern % (
                url_for('frontend.people', id=self.from_id), Markup.escape(self.from_people.nickname),
            )

