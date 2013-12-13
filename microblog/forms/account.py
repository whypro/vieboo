# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, HiddenField, SubmitField, FileField, RadioField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Optional, Regexp, URL
from microblog.models import People
from microblog.models.account import gender_enum, sexual_orientation_enum, blood_type_enum, profession_enum, education_enum

_mobile_regexp = '((\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)'
_zip_regexp = '\d{6}'

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
        u'手机', validators=[Optional(), Regexp(_mobile_regexp, message=u'请输入一个合法的号码')]
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
    # email = TextField(u'邮箱', validators=[Email(message=u'请输入一个合法的邮箱')],)
    # password = PasswordField(u'密码',)

    nickname = TextField(
        u'昵称',
        validators=[DataRequired(message=u'请输入昵称')],
    )
    mobile = TextField(
        u'手机',
        validators=[Optional(), Regexp(_mobile_regexp, message=u'请输入一个合法的号码')],
    )
    next = HiddenField()
    submit = SubmitField(u'修改')

    # def validate_email(self, field):
    #    if g.user.get_email() != field.data:
    #        raise ValidationError(u'邮箱不能修改')


class ModifyProfileDetailForm(Form):

    _gender_choices = [(item, item) for item in gender_enum]
    _sexual_orientation_choices = [(item, item) for item in sexual_orientation_enum]
    _blood_type_choices = [(item, item) for item in blood_type_enum]
    _profession_choices = [(item, item) for item in profession_enum]
    _education_choices = [(item, item) for item in education_enum]

    fullname = TextField(u'姓名')
    gender = RadioField(u'性别', choices=_gender_choices)
    sexual_orientation = SelectField(u'性取向', choices=_sexual_orientation_choices)
    birthday = DateField(u'生日', validators=[Optional()],)
    blood_type = SelectField(u'血型', choices=_blood_type_choices)    # 血型
    profession = SelectField(u'职业', choices=_profession_choices)
    education = SelectField(u'学历', choices=_education_choices)
    school = TextField(u'毕业院校')
    homepage = TextField(u'个人网站', validators=[Optional(), URL(message=u'请输入一个合法的 URL，例如：http://www.douban.com')])
    hometown = TextField(u'故乡')
    location = TextField(u'所在地')
    address = TextField(u'地址')
    zip_code = TextField(u'邮编', validators=[Optional(), Regexp(_zip_regexp, message=u"请输入一个合法的邮编")])
    qq = TextField('QQ')
    introduction = TextAreaField(u'个人简介')
    submit = SubmitField(u'修改')


class AvatarForm(Form):
    avatar = FileField(u'头像')
    avatar_uri = TextField(u'头像网络地址')
    submit = SubmitField(u'上传')