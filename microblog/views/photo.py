# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from flask import Blueprint, flash, redirect, url_for, request, g, current_app, \
    abort
from flask.ext.login import login_required
from sqlalchemy import and_
from microblog.forms.photo import PhotoForm
from microblog.models import PhotoAlbum
from microblog.extensions import db
from microblog.forms import UploadForm, ModifyAlbumForm, AddAlbumForm
from microblog.helpers import render_template, get_uploader
from microblog.models import Photo


photo = Blueprint('photo', __name__, url_prefix='')


@photo.route('/album/add/', methods=['GET', 'POST'])
@login_required
def add_album():
    """新建相册"""
    add_album_form = AddAlbumForm()
    if add_album_form.validate_on_submit():
        album = PhotoAlbum(
            title=add_album_form.title.data,
            description=add_album_form.description.data,
            people_id=g.user.id
        )
        db.session.add(album)
        db.session.commit()
        flash('相册新建成功', 'success')
        return redirect(url_for('show_album', id=album.id))
        # return '添加成功'

    return render_template(
        'photo/album-info.html',
        form=add_album_form,
        title='新建相册'
    )


@photo.route('/album/<int:id>/')
@login_required
def show_album(id):
    """显示相册里的所有照片，只能查看自己的相册"""
    album = PhotoAlbum.query.get_or_404(id)
    #if album.people_id != g.user.id:
    #    flash('权限不足', 'warning')
    #    return redirect(url_for('frontend.index'))
    return render_template(
        'photo/album.html',
        album=album,
        title='查看相册'
    )


@photo.route('/album/<int:id>/modify/', methods=['GET', 'POST'])
@login_required
def modify_album(id):
    """修改相册属性"""
    album = PhotoAlbum.query.get_or_404(id)
    if album.people_id != g.user.id:
        flash('权限不足', 'warning')
        return redirect(url_for('show_album', id=album.id))
    if album.title == '默认相册':
        flash('无法修改属性', 'warning')
        return redirect(url_for('show_album', id=album.id))
    modify_album_form = ModifyAlbumForm(obj=album)
    if modify_album_form.validate_on_submit():
        album.title = modify_album_form.title.data
        album.description = modify_album_form.description.data

        db.session.add(album)
        db.session.commit()
        flash('相册修改成功', 'success')
        return redirect(url_for('show_album', id=album.id))

    return render_template(
        'photo/album-info.html',
        form=modify_album_form,
        title='修改相册属性'
    )


@photo.route('/album/<int:id>/delete/')
@login_required
def delete_album(id):
    """删除相册"""
    clear_album = request.args.get('clear')
    print clear_album
    album = PhotoAlbum.query.get_or_404(id)

    if album.people_id != g.user.id:
        flash('删除失败', 'warning')
        return redirect(url_for('frontend.album', id=g.user.id))
    if album.title == '默认相册':
        flash('无法删除默认相册', 'warning')
        return redirect(url_for('frontend.album', id=g.user.id))

    if clear_album == '1':
        # 删除相册内的照片
        print 'delete photos'
        for photo in album.photos:
            db.session.delete(photo)
            db.session.commit()
    else:
        # 移入默认相册
        # TODO: commit 需要重新考虑
        default_album = PhotoAlbum.query.filter_by(title='默认相册').first()
        if not default_album:
            # 如果没有默认相册，则新建一个默认相册
            default_album = PhotoAlbum(
                title='默认相册',
                people_id=g.user.id
            )
            db.session.add(default_album)
            db.session.commit()
        for photo in album.photos:
            photo.album_id = default_album.id
            db.session.add(photo)
            db.session.commit()

    db.session.delete(album)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('frontend.album', id=g.user.id))


@photo.route('/album/upload/', methods=['GET', 'POST'])
@photo.route('/album/<int:id>/upload/', methods=['GET', 'POST'])
@login_required
def upload_photo(id=None):
    if id:
        album = PhotoAlbum.query.get_or_404(id)
        if album.people_id != g.user.id:
            flash('权限不足', 'warning')
            return redirect('frontend.index')
    # 列出所有相册
    album_choices = [(str(a.id), a.title) for a in g.user.albums]
    if not album_choices:
        # 如果没有任何相册，则新建一个默认相册
        default_album = PhotoAlbum(
            title='默认相册',
            people_id=g.user.id
        )
        db.session.add(default_album)
        db.session.commit()
        album_choices.append((str(default_album.id), default_album.title))
        
    upload_form = UploadForm()
    upload_form.album.choices = album_choices
    if not id:
        id = album_choices[0][0]    # 第一个相册的 id
    upload_form.album.data = str(id)
    
    if upload_form.validate_on_submit():
        print 'id:', upload_form.album.data
        album = PhotoAlbum.query.get_or_404(upload_form.album.data)
        if album.people_id != g.user.id:
            flash('权限不足', 'warning')
            return redirect('frontend.index')
         # 循环上传照片
        for field in upload_form:
            print field.name
            if 'photo' in field.name and field.data:
                photo_data = request.files[field.name]
                uploader = get_uploader()
                filename = uploader.save(photo_data)
                if not filename:
                    flash('上传失败', 'danger')
                    return redirect(url_for('frontend.album', id=g.user.id))
                print upload_form.album.data
                photo = Photo(uri=filename, album_id=upload_form.album.data, people_id=g.user.id)
                db.session.add(photo)
                db.session.commit()
        flash('上传成功', 'success')
        return redirect(url_for('frontend.album', id=g.user.id))

    return render_template(
        'photo/upload.html',
        form=upload_form,
        title='上传照片'
    )


@photo.route('/photo/<int:pid>/')
@photo.route('/album/<int:aid>/photo/<int:pid>/')
def show_photo(pid, aid=None):
    photo = Photo.query.get_or_404(pid)
    prev_id = next_id = None
    if aid:
        if photo.album_id != aid:
            abort(404)
        else:
            # 获取 prev_id & next_id
            # 上一张和下一张
            prev_photo = Photo.query.filter(and_(Photo.id<pid, Photo.album_id==aid)).order_by(Photo.id.desc()).first()
            if prev_photo:
                prev_id = prev_photo.id
            next_photo = Photo.query.filter(and_(Photo.id>pid, Photo.album_id==aid)).first()
            if next_photo:
                next_id = next_photo.id
    return render_template(
        'photo/photo.html',
        photo=photo,
        prev_id=prev_id,
        next_id=next_id,
        title='查看照片'
    )


@photo.route('/photo/<int:id>/modify/', methods=['GET', 'POST'])
@login_required
def modify_photo(id):
    photo = Photo.query.get_or_404(id)
    if photo.people_id != g.user.id:
        flash('权限不足', 'warning')
        return redirect(url_for('frontend.index'))
    photo_form = PhotoForm(obj=photo)
    if photo_form.validate_on_submit():
        photo.description = photo_form.description.data
        db.session.add(photo)
        db.session.commit()
        flash('修改成功', 'success')
        return redirect(url_for('show_photo', id=id))
    return render_template(
        'photo/photo-info.html',
        form=photo_form,
        title='修改照片属性'
    )


@photo.route('/photo/<int:id>/delete/')
@login_required
def delete_photo(id):
    """删除照片"""
    photo = Photo.query.get_or_404(id)
    if photo.people_id != g.user.id:
        flash('删除失败', 'warning')
        return redirect(url_for('show_photo', id=id))
    print photo.uri
    uploader = get_uploader()
    uploader.remove(photo.uri)

    db.session.delete(photo)
    db.session.commit()
    flash('删除成功', 'success')
    if photo.album_id:
        return redirect(url_for('photo.show_album', id=photo.album_id))
    else:
        return redirect(url_for('frontend.album', id=g.user.id))


@photo.route('/photo/<int:pid>/move/<int:aid>/')
@login_required
def move_to_album(pid, aid):
    pass


@photo.route('/photo/<int:pid>/comment/')
@photo.route('/photo/<int:pid>/comment/<int:cid>/')
@login_required
def comment_photo(pid, cid):
    pass


@photo.route('/photo/comment/<int:id>/delete/')
@login_required
def delete_comment(id):
    pass

