# -*- coding: utf-8 -*-
from microblog.database import db
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
    content = db.Column(db.Text, nullable=False)
    post_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, people_id, content):
        self.people_id = people_id
        self.content = content
