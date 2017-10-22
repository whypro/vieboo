# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, TextField
from wtforms.validators import DataRequired


class ChatForm(Form):
    content = TextAreaField(u'内容', validators=[DataRequired(message=u'请输入聊天内容')])
    submit = SubmitField(u'发送')


class AddGroupForm(Form):
    name = TextField(
        u'名称',
        validators=[DataRequired(message=u'请输入分组名称')],
    )
    submit = SubmitField(u'新建')


class RenameGroupForm(AddGroupForm):
    submit = SubmitField(u'修改')