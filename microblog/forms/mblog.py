# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(Form):
    content = TextAreaField(u'内容', validators=[DataRequired(message=u'请输入微博内容')])
    submit = SubmitField(u'发布')


class CommentForm(Form):
    content = TextAreaField(u'内容', validators=[DataRequired(message=u'请输入评论内容')])
    submit = SubmitField(u'评论')

