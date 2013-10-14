# -*- coding: utf-8 -*-
from flask import g
from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, HiddenField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from microblog.models import People


class LoginForm(Form):
    login = TextField(
        u'邮箱',
        validators=[DataRequired(message=u'请输入邮箱')],
    )
    password = PasswordField(
        u'密码',
        validators=[DataRequired(message=u'请输入密码')],
    )
    remember = BooleanField(u'记住我')
    next = HiddenField()
    submit = SubmitField(u'登录')


class RegisterForm(Form):
    email = TextField(
        u'邮箱',
        validators=[DataRequired(message=u'请输入邮箱'),
                    Email(message=u'请输入一个合法的邮箱')],
    )
    password = PasswordField(
        u'密码',
        validators=[DataRequired(message=u'请输入密码'),
                    EqualTo('password_confirm', message=u'两次密码不一致')],
    )
    password_confirm = PasswordField(
        u'确认密码',
        validators=[DataRequired(message=u'请再次输入密码'),
                    EqualTo('password', message=u'两次密码不一致')],
    )
    nickname = TextField(
        u'昵称',
        validators=[DataRequired(message=u'请输入昵称')],
    )
    mobile = TextField(
        u'手机',
    )
    next = HiddenField()
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        people = People.query.filter(People.email.like(field.data)).first()
        if people:
            raise ValidationError(u'用户名已存在')


class ChangePasswordForm(Form):
    password_old = PasswordField(
        u'原密码',
        validators=[DataRequired(message=u'请输入原密码')],
    )
    password_new = PasswordField(
        u'新密码',
        validators=[DataRequired(message=u'请输入新密码'),
                    EqualTo('password_confirm', message=u'两次密码不一致')],
    )
    password_confirm = PasswordField(
        u'确认新密码',
        validators=[DataRequired(message=u'请再次输入新密码'),
                    EqualTo('password_new', message=u'两次密码不一致')],
    )
    next = HiddenField()
    submit = SubmitField(u'确定')


class ModifyProfileForm(Form):
    email = TextField(
        u'邮箱',
        validators=[Email(message=u'请输入一个合法的邮箱')],
    )
    password = PasswordField(
        u'密码',
    )

    nickname = TextField(
        u'昵称',
    )
    mobile = TextField(
        u'手机',
    )
    next = HiddenField()
    submit = SubmitField(u'修改')

    def validate_email(self, field):
        if g.user.get_email() != field.data:
            raise ValidationError(u'邮箱不能修改')