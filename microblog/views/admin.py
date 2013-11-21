# -*- coding: utf-8 -*-
from flask import Module, flash, redirect, url_for
from microblog.extensions import db

admin = Module(__name__)

@admin.route('/')
def index():
    return u'未完成'


@admin.route('/install/')
def install():
    db.create_all()
    flash(u'创建成功', 'success')
    return redirect(url_for('index'))