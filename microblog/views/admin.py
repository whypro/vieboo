# -*- coding: utf-8 -*-
from flask import Module

admin = Module(__name__)

@admin.route('/')
def index():
    return u'未完成'