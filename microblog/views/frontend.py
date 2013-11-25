# -*- coding: utf-8 -*-
from flask import Module, g, url_for, redirect, flash, send_from_directory, current_app, abort
from microblog.models import People, Microblog
from microblog.helpers import render_template
from microblog.forms import PostForm

frontend = Module(__name__)

@frontend.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@frontend.route('/')
def index():
    if g.user.is_authenticated():
        # 黑名单不显示
        microblogs = Microblog.query.filter(~Microblog.people_id.in_([p.id for p in g.user.blocking])).order_by(Microblog.post_time.desc()).limit(10).all()
    else:
        microblogs = Microblog.query.order_by(Microblog.post_time.desc()).limit(10).all()
    # print microblogs
    return render_template('index.html', microblogs=microblogs, post_form=PostForm())


@frontend.route('/people/<int:id>/')
def people(id):
    people = People.query.get_or_404(id)
    return render_template('people.html', people=people)


@frontend.route('/uploads/photos/<filename>')
def uploads(filename):
    return send_from_directory(
        current_app.config['UPLOADED_PHOTOS_DEST'],
        filename
    )


@frontend.route('/test/<int:error>/')
def test(error):
    """HTTP 错误测试"""
    if error in (404, 500):
        abort(error)
    else:
        return redirect(url_for('frontend.index'))