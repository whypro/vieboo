# -*- coding: utf-8 -*-
import datetime
from microblog.database import db


Friendship = db.Table(
    'friendship',
    db.Column('from_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('to_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('follow_time', db.DateTime, default=datetime.datetime.now)
)

