# -*- coding: utf-8 -*-
from flask import Module, g, url_for, redirect, send_from_directory, current_app, abort, request
from microblog.models import People, Microblog, PhotoAlbum, Photo
from microblog.helpers import render_template
from microblog.forms import PostForm

frontend = Module(__name__)

@frontend.route('/favicon.ico')
def favicon():
    return send_from_directory(
        'static',
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


@frontend.route('/')
def index():
    if g.user.is_authenticated():
        # 只显示关注的人
        microblogs = Microblog.query.\
            filter(Microblog.people_id.in_([p.id for p in g.user.following]+[g.user.id])).\
            order_by(Microblog.post_time.desc()).limit(10).all()
    else:
        microblogs = Microblog.query.order_by(Microblog.post_time.desc()).limit(10).all()
    # print microblogs
    return render_template('index.html', microblogs=microblogs, post_form=PostForm())


@frontend.route('/square/')
def square():
    microblogs = Microblog.query.order_by(Microblog.post_time.desc()).limit(10).all()
    # print microblogs
    return render_template('square.html', microblogs=microblogs, post_form=PostForm())


@frontend.route('/people/<int:id>/')
def people(id):
    people = People.query.get_or_404(id)
    return render_template('people.html', people=people)


@frontend.route('/people/<int:id>/album/')
def album(id):
    people = People.query.get_or_404(id)
    albums = PhotoAlbum.query.filter_by(people_id=id).all()
    # default_album_photos = Photo.query.filter_by(people_id=id).all()
    return render_template('photo/all-albums.html', albums=albums, people=people, title=u'所有相册')


@frontend.route('/people/<int:id>/album/default/')
def default_album(id):
    people = People.query.get_or_404(id)
    default_album_photos = Photo.query.filter_by(people_id=id, album_id=None).all()
    return render_template(
        'photo/default-album.html',
        people=people,
        photos=default_album_photos,
        title=u'默认相册'
    )


@frontend.route('/uploads/photos/<filename>')
def uploads(filename):
    if not current_app.config['USE_BCS_BUCKET']:
        return send_from_directory(
            current_app.config['UPLOADS_DIR'],
            filename
        )
    else:
        return redirect(
            'http://bcs.duapp.com/' +
            current_app.config['BCS_BUCKET_NAME'] +
            '/' + filename
        )


@frontend.route('/remote/photo/')
def remote_photo():
    uri = request.args.get('uri', None)
    return redirect(uri)


@frontend.route('/test/<int:error>/')
def test(error):
    """HTTP 错误测试"""
    if error in (404, 500):
        abort(error)
    else:
        return redirect(url_for('frontend.index'))