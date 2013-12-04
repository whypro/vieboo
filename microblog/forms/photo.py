# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, FileField, TextField
from wtforms.validators import DataRequired


class UploadForm(Form):
    photo_1 = FileField(u'图片1')
    photo_2 = FileField(u'图片2')
    photo_3 = FileField(u'图片3')
    photo_4 = FileField(u'图片4')
    photo_5 = FileField(u'图片5')
    submit = SubmitField(u'上传')


class AddAlbumForm(Form):
    title = TextField(
        u'相册名称',
        validators=[DataRequired(message=u'请输入相册名称')]
    )
    description = TextAreaField(u'相册描述')
    submit = SubmitField(u'新建')


class ModifyAlbumForm(AddAlbumForm):
    submit = SubmitField(u'修改')

