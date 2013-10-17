# -*- coding: utf-8 -*-
import datetime
from microblog.database import db


friendship = db.Table(
    'friendship',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('from_id', db.Integer, db.ForeignKey('people.id')),
    db.Column('to_id', db.Integer, db.ForeignKey('people.id')),
    db.Column('follow_time', db.DateTime, default=datetime.datetime.now)
)

