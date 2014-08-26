# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint
from microblog.helpers import render_template, get_mongodb


sinaweibo = Blueprint('sinaweibo', __name__, url_prefix='/sinaweibo')



sinaweibo.route('/')
def index():
    return 'hehe'
    connection = get_mongodb()
    statuses = connection.Status.find().sort([('reposts_count', -1)])
    return render_template('mongodb/index.html', statuses=statuses)


