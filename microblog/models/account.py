# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import BaseQuery
from microblog.extensions import db
import datetime
import hashlib
from microblog.helpers import render_uri
from microblog.models.friendship import Friendship, Blackship, Chatting


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
    nickname = db.Column(db.String(20), unique=True)
    mobile = db.Column(db.String(20))
    reg_time = db.Column(db.DateTime, default=datetime.datetime.now)
    reg_ip = db.Column(db.String(20))
    status = db.Column(db.String(10), default='active')
    avatar = db.Column(db.String(255))

    microblogs = db.relationship('Microblog', backref='people', lazy='dynamic', order_by='Microblog.post_time.desc()')
    comments = db.relationship(
        'Comment',
        backref='people',
        lazy='dynamic',
        order_by='Comment.comment_time'
    )

    following = db.relationship(
        'People',
        secondary=Friendship,
        primaryjoin=id==Friendship.c.from_id,
        secondaryjoin=id==Friendship.c.to_id,
        backref=db.backref('followed', lazy='dynamic'),
        lazy='dynamic',
    )
    blocking = db.relationship(
        'People',
        secondary=Blackship,
        primaryjoin=id==Blackship.c.from_id,
        secondaryjoin=id==Blackship.c.to_id,
        backref=db.backref('blocked', lazy='dynamic'),
        lazy='dynamic'
    )

    groups = db.relationship(
        'Group',
        backref='people',
        lazy='dynamic',
        passive_deletes=True
    )

    sent_chattings = db.relationship(
        'Chatting', backref='from_people',
        primaryjoin=id==Chatting.from_id,
        lazy='dynamic')
    received_chattings = db.relationship(
        'Chatting',
        backref='to_people',
        primaryjoin=id==Chatting.to_id,
        lazy='dynamic')

    login_logs = db.relationship(
        'LoginLog',
        backref='people',
        lazy='dynamic',
        passive_deletes=True,
    )

    roles = db.relationship('Role', secondary='people_roles')

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

    def is_admin(self):
        for role in self.roles:
            if role.name == 'admin':
                return True
        return False

    def get_nickname(self):
        return self.nickname

    def get_email(self):
        return self.email

    def get_avatar_uri(self):
        if self.avatar:
            return render_uri(self.avatar)
        else:
            return None

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
            (Friendship.c.from_id == self.id) &
            (Friendship.c.to_id == id)
        ).first()
        return True if people else False

    def is_blocking(self, id):
        people = self.blocking.filter(
            (Blackship.c.from_id == self.id) &
            (Blackship.c.to_id == id)
        ).first()
        return True if people else False

    def has_group(self, id):
        group = self.groups.filter_by(id=id).first()
        return True if group else False

    def __repr__(self):
        return self.email

    def get_mutual(self):
        return self.followed.filter(Friendship.c.to_id==self.id)


class LoginLog(db.Model):
    __tablename__ = 'login_log'
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(
        db.Integer,
        db.ForeignKey(People.id, ondelete='CASCADE'),
        nullable=True
    )
    login_time = db.Column(db.DateTime, default=datetime.datetime.now)
    login_ip = db.Column(db.String(20))

    def __init__(self, people_id, login_ip):
        self.people_id = people_id
        self.login_ip = login_ip


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))


people_roles = db.Table(
    'people_roles',
    db.Column('people_id', db.Integer, db.ForeignKey('people.id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), primary_key=True),
)


gender_enum = (u'男', u'女')
sexual_orientation_enum = (u'男', u'女')
profession_enum = (u'在校学生', u'固定工作者', u'自由职业者', u'待业', u'退休')
education_enum = (u'小学及以下', u'初中', u'高中', u'中专', u'大专', u'本科', u'研究生', u'博士及以上')
chinese_zodiac_enum = (
    u'鼠', u'牛', u'虎', u'兔', u'龙', u'蛇',
    u'马', u'羊', u'猴', u'鸡', u'狗', u'猪'
)
star_sign_enum = (
    u'白羊座', u'金牛座', u'双子座', u'巨蟹座', u'狮子座', u'处女座',
    u'天秤座', u'天蝎座', u'射手座', u'摩羯座', u'水瓶座', u'双鱼座'
)
blood_type_enum = (u'A型', u'B型', u'AB型', u'O型')


class PeopleInfo(db.Model):
    __tablename__ = 'people_info'

    id = db.Column(db.Integer, db.ForeignKey('people.id'), primary_key=True)
    fullname = db.Column(db.String(20))
    gender = db.Column(db.Enum(u'男', u'女'))    # 性别，False: Female, True: Male
    sexual_orientation = db.Column(db.Enum(u'男', u'女'))    # 性取向
    birthday = db.Column(db.Date)   # 生日
    age = db.Column(db.SmallInteger)    # 年龄，触发器
    chinese_zodiac = db.Column(db.Enum(
        u'鼠', u'牛', u'虎', u'兔', u'龙', u'蛇',
        u'马', u'羊', u'猴', u'鸡', u'狗', u'猪'))    # 生肖，触发器
    star_sign = db.Column(db.Enum(
        u'白羊座', u'金牛座', u'双子座', u'巨蟹座', u'狮子座', u'处女座',
        u'天秤座', u'天蝎座', u'射手座', u'摩羯座', u'水瓶座', u'双鱼座'))      # 星座，触发器
    blood_type = db.Column(db.Enum(u'A型', u'B型', u'AB型', u'O型'))    # 血型
    profession = db.Column(db.String(20))   # 职业
    education = db.Column(db.String(20))    # 学历
    school = db.Column(db.String(80))       # 毕业院校
    homepage = db.Column(db.String(255))    # 个人网站
    hometown = db.Column(db.String(20))     # 故乡
    location = db.Column(db.String(20))     # 所在地
    address = db.Column(db.String(100))     # 地址
    zip_code = db.Column(db.String(10))     # 邮编
    qq = db.Column(db.String(20))           # QQ 号码
    introduction = db.Column(db.Text)          # 个人简介

    people = db.relationship('People', backref=db.backref('info', uselist=False), uselist=False)

    def __init__(self, id, fullname, gender, sexual_orientation, birthday,
                 blood_type, profession, education, school, homepage, hometown, location,
                 address, zip_code, qq, introduction):
        self.id = id
        self.fullname = fullname
        self.gender = gender
        self.sexual_orientation = sexual_orientation
        self.birthday = birthday
        self.blood_type = blood_type
        self.profession = profession
        self.education = education
        self.school = school
        self.homepage = homepage
        self.hometown = hometown
        self.location = location
        self.address = address
        self.zip_code = zip_code
        self.qq = qq
        self.introduction = introduction

    def change_info(self, fullname, gender, sexual_orientation, birthday,
                    blood_type, profession, education, school, homepage, hometown, location,
                    address, zip_code, qq, introduction):
        self.fullname = fullname
        self.gender = gender
        self.sexual_orientation = sexual_orientation
        self.birthday = birthday
        self.blood_type = blood_type
        self.profession = profession
        self.education = education
        self.school = school
        self.homepage = homepage
        self.hometown = hometown
        self.location = location
        self.address = address
        self.zip_code = zip_code
        self.qq = qq
        self.introduction = introduction

    def update_age(self):
        # 计算年龄
        pass

    def update_chinese_zodiac(self):
        # 计算生肖
        pass

    def update_star_sign(self):
        # 计算星座
        pass

