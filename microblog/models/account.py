# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import BaseQuery
from microblog.database import db
import datetime
import hashlib
from microblog.models.friendship import Friendship, Blackship


class PeopleQuery(BaseQuery):
    def authenticate(self, login, password):
        _password = hashlib.md5(password).hexdigest()
        people = People.query.filter(
            (People.email==login) &
            (People._password==_password)
        ).first()
        return people

    def exists(self, login):
        people = People.query.filter(
            (People.email==login)
        ).first()
        return True if people else False


class People(db.Model):
    __tablename__ = 'people'
    query_class = PeopleQuery

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column('password', db.String(80), nullable=False)
    nickname = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    reg_time = db.Column(db.DateTime, default=datetime.datetime.now)
    reg_ip = db.Column(db.String(20))
    avatar = db.Column(db.String(255))

    microblogs = db.relationship('Microblog', backref='people', lazy='dynamic')
    comments = db.relationship('Comment', backref='people', lazy='dynamic')

    following = db.relationship(
        'People',
        secondary=Friendship,
        primaryjoin=id==Friendship.c.from_id,
        secondaryjoin=id==Friendship.c.to_id,
        backref=db.backref('followed', lazy='dynamic'),
        lazy='dynamic'
    )
    blocking = db.relationship(
        'People',
        secondary=Blackship,
        primaryjoin=id==Blackship.c.from_id,
        secondaryjoin=id==Blackship.c.to_id,
        backref=db.backref('blocked', lazy='dynamic'),
        lazy='dynamic'
    )

    groups = db.relationship('Group', backref='people', lazy='dynamic', passive_deletes=True)

    def __init__(self, email, password,
                 nickname=None, mobile=None,
                 reg_time=None, reg_ip=None):
        self.email = email
        self._password = hashlib.md5(password).hexdigest()
        self.nickname = nickname
        self.mobile = mobile
        self.reg_time = reg_time
        self.reg_ip = reg_ip

    def __repr__(self):
        return ''

    # flask.ext.login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    # flask.ext.login

    def get_nickname(self):
        return self.nickname

    def get_email(self):
        return self.email

    def get_avatar(self):
        return self.avatar

    def change_password(self, password):
        self._password = hashlib.md5(password).hexdigest()

    def change_nickname(self, nickname):
        self.nickname = nickname

    def change_mobile(self, mobile):
        self.mobile = mobile

    def change_avatar(self, avatar):
        self.avatar = avatar

    def is_following(self, id):
        people = self.following.filter(
            (Friendship.c.from_id==self.id) &
            (Friendship.c.to_id==id)
        ).first()
        return True if people else False

    def is_blocking(self, id):
        people = self.blocking.filter(
            (Blackship.c.from_id==self.id) &
            (Blackship.c.to_id==id)
        ).first()
        return True if people else False

    def __repr__(self):
        return self.email


class LoginLog(db.Model):
    __tablename__ = 'login_log'
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, nullable=True)
    login_time = db.Column(db.DateTime, default=datetime.datetime.now)
    login_ip = db.Column(db.String(20))

    def __init__(self, people_id, login_ip):
        self.people_id = people_id
        self.login_ip = login_ip
