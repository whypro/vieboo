# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(Form):
    content = TextAreaField(u'内容', validators=[DataRequired(message=u'请输入聊天内容')])
    submit = SubmitField(u'发送')