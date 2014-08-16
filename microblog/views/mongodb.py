# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint
from mongokit import Connection, Document
from microblog.helpers import render_template


mongodb = Blueprint('mongodb', __name__, url_prefix='/mongodb')


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

connection = Connection(MONGODB_HOST, MONGODB_PORT)

@connection.register
class Status(Document):
    __database__ = 'weibo_analyzer'
    __collection__ = 'status'
    
    structure = {
        'create_at': basestring, 
        'id': int, 
        'mid': int,
        'idstr': basestring, 
        'text': basestring, 
        'source': basestring,
        'favorited': bool, 
        'truncated': bool, 
        'in_reply_to_status_id': basestring, 
        'in_reply_to_user_id': basestring, 
        'in_reply_to_screen_name': basestring, 
        'thumbnail_pic': basestring, 
        'bmiddle_pic': basestring, 
        'original_pic': basestring, 
        'geo': None, 
        'user': None, 
        'retweeted_status': None, 
        'reposts_count': int, 
        'comments_count': int, 
        'attitudes_count': int, 
        'mlevel': int, 
        'visible': None, 
        'pic_urls': None, 
        'ad': list,
    }
    use_autorefs = True

@connection.register
class User(Document):
    structure = {
        'id': int,
        'idstr': basestring, 
        'screen_name': basestring, 
        'name': basestring, 
        'province': int, 
        'city': int, 
        'location': basestring, 
        'description': basestring,
        'url': basestring, 
        'profile_image_url': basestring, 
        'domain': basestring, 
        'weihao': basestring, 
        'gender': basestring, 
        'followers_count': int, 
        'friends_count': int, 
        'statuses_count': int, 
        'favourites_count': int, 
        'created_at': basestring, 
        'following': bool, 
        'allow_all_act_msg': bool, 
        'geo_enabled': bool, 
        'verified': bool, 
        'verified_type': int, 
        'remark': basestring, 
        'status': Status, 
        'allow_all_comment': bool, 
        'avatar_large': basestring, 
        'avatar_hd': basestring, 
        'verified_reason': basestring, 
        'follow_me': bool, 
        'online_status': int, 
        'bi_followers_count': int, 
        'lang': basestring,
    }
    use_autorefs = True


@mongodb.route('/')
def index():
    statuses = connection.Status.find().sort([('reposts_count', -1)])
    return render_template('mongodb/index.html', statuses=statuses)


