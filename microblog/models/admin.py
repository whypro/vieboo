# -*- coding: utf-8 -*-
__author__ = 'whypro'
from microblog.database import db


class Admin(db.Model):
    __tablename__ = 'people'