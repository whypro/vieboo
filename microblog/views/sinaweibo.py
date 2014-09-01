# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from flask import Blueprint, abort
from microblog.helpers import render_template, get_mongodb
from microblog.models import Status

sinaweibo = Blueprint('sinaweibo', __name__, url_prefix='/sinaweibo')



@sinaweibo.route('/', defaults={'page': 1})
@sinaweibo.route('/page/<int:page>/')
def index(page):
    connection = get_mongodb()
    connection.register([Status])

    page_count = 10
    start = page_count * (page - 1)
    max_page = connection.Status.find().count() // page_count
    if page < 1 or page > max_page:
        abort(404)

    # statuses = connection.Status.find().sort([('reposts_count', -1)]).skip(start).limit(page_count)
    statuses = connection.Status.find().sort([('_id', -1)]).skip(start).limit(page_count)
    return render_template('sinaweibo/index.html', statuses=statuses, page=page, max_page=max_page)
