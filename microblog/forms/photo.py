# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, FileField, TextField, SelectField
from wtforms.validators import DataRequired, NoneOf


class UploadForm(Form):
    album = SelectField(u'相册')
    photo_1 = FileField(u'图片1')
    photo_2 = FileField(u'图片2')
    photo_3 = FileField(u'图片3')
    photo_4 = FileField(u'图片4')
    photo_5 = FileField(u'图片5')
    submit = SubmitField(u'上传')


class AddAlbumForm(Form):
    title = TextField(
        u'相册名称',
        validators=[DataRequired(message=u'请输入相册名称'), NoneOf([u'默认相册'], message=u'相册名称不合法')]
    )
    description = TextAreaField(u'相册描述')
    submit = SubmitField(u'新建')


class ModifyAlbumForm(AddAlbumForm):
    submit = SubmitField(u'修改')


class PhotoForm(Form):
    description = TextAreaField(u'照片描述')
    submit = SubmitField(u'修改')