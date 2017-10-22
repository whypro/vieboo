# -*- coding: utf-8 -*-
__author__ = 'whypro'
from microblog.extensions import db
import datetime


class VisitLog(db.Model):
    __tablename__ = 'visit_log'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10))   # GET, POST, PUT, DELETE
    referrer = db.Column(db.String(255))
    platform = db.Column(db.String(80))
    browser = db.Column(db.String(80))
    version = db.Column(db.String(20))
    client_ip = db.Column(db.String(20))
    visit_time = db.Column(db.DateTime, default=datetime.datetime.now)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='SET NULL'))

    people = db.relationship('People', uselist=False)

    def __init__(self, url, method, referrer, platform, browser, version, client_ip, visit_time, people_id):
        self.url = url
        self.referrer = referrer
        self.method = method
        self.platform = platform
        self.browser = browser
        self.version = version
        self.client_ip = client_ip
        self.visit_time = visit_time
        self.people_id = people_id

