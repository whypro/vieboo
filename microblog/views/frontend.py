# -*- coding: utf-8 -*-
from flask import Module, url_for, redirect, flash, send_from_directory, current_app
from microblog.database import db
from microblog.models import People, Microblog
from microblog.tools import render_template
from microblog.forms import LoginForm, PostForm

frontend = Module(__name__)

@frontend.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@frontend.route('/')
def index():
    # TODO: 黑名单不显示
    microblogs = Microblog.query.order_by(Microblog.post_time.desc()).limit(10).all()
    # print microblogs
    return render_template('index.html', microblogs=microblogs, post_form=PostForm())


@frontend.route('/install/')
def install():
    db.create_all()
    flash(u'创建成功', 'success')
    return redirect(url_for('index'))


@frontend.route('/people/<int:id>/')
def people(id):
    people = People.query.get(id)
    return render_template('people.html', people=people)


@frontend.route('/uploads/photos/<filename>')
def uploads(filename):
    return send_from_directory(
        current_app.config['UPLOADED_PHOTOS_DEST'],
        filename
    )



@frontend.route('/test/')
def test():
    return render_template('test.html')