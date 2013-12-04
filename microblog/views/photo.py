# -*- coding: utf-8 -*-
import os
from flask import Module, flash, redirect, url_for, request, g
from flask.ext.login import login_required
from microblog.models import PhotoAlbum
from microblog.extensions import photos, db
from microblog.forms import UploadForm, ModifyAlbumForm, AddAlbumForm
from microblog.helpers import render_template
from microblog.models import Photo

photo = Module(__name__, url_prefix='')


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
        flash(u'相册新建成功', 'success')
        return redirect(url_for('show_album', id=album.id))
        # return u'添加成功'

    return render_template(
        'photo/album-info.html',
        form=add_album_form,
        title=u'新建相册'
    )


@photo.route('/album/<int:id>/')
@login_required
def show_album(id):
    """显示相册里的所有照片，只能查看自己的相册"""
    album = PhotoAlbum.query.get_or_404(id)
    if album.people_id != g.user.id:
        flash(u'权限不足', 'warning')
        return redirect('frontend.index')
    photos = Photo.query.filter_by(album_id=id).all()
    return render_template(
        'photo/album.html',
        photos=photos,
        album=album,
        title=u'查看相册'
    )


@photo.route('/album/<int:id>/modify/', methods=['GET', 'POST'])
@login_required
def modify_album(id):
    """修改相册属性"""
    album = PhotoAlbum.query.get_or_404(id)
    modify_album_form = ModifyAlbumForm(obj=album)
    if modify_album_form.validate_on_submit():
        album.title = modify_album_form.title.data
        album.description = modify_album_form.description.data

        db.session.add(album)
        db.session.commit()
        flash(u'相册修改成功', 'success')
        return redirect(url_for('show_album', id=album.id))

    return render_template(
        'photo/album-info.html',
        form=modify_album_form,
        title=u'修改相册'
    )


@photo.route('/album/<int:id>/delete/')
@login_required
def delete_album(id):
    """删除相册"""
    album = PhotoAlbum.query.get_or_404(id)
    if album.people_id == g.user.id:
        db.session.delete(album)
        # TODO: 删除相册内的照片
        db.session.commit()
        flash(u'删除成功', 'success')
    else:
        flash(u'删除失败', 'warning')
    return redirect(url_for('frontend.album', id=g.user.id))


@photo.route('/album/<int:id>/upload/', methods=['GET', 'POST'])
@login_required
def upload_photo(id):
    album = PhotoAlbum.query.get_or_404(id)
    if album.people_id != g.user.id:
        flash(u'权限不足', 'warning')
        return redirect('frontend.index')
    upload_form = UploadForm()
    # print upload_form.submit.name
    if upload_form.validate_on_submit():
         # 循环上传照片
        for field in upload_form:
            print field.name
            if 'photo' in field.name and field.data:
                avatar_data = request.files[field.name]
                avatar_filename = photos.save(avatar_data)
                photo = Photo(uri=avatar_filename, album_id=id)
                db.session.add(photo)
                db.session.commit()
        flash(u'上传成功', 'success')
        return redirect(url_for('photo.show_album', id=id))
    return render_template(
        'photo/upload.html',
        form=upload_form,
        title=u'上传照片'
    )


@photo.route('/photo/<int:id>/')
def show_photo(id):
    photo = Photo.query.get_or_404(id)
    return render_template(
        'photo/photo.html',
        photo=photo,
        title=u'查看照片'
    )


@photo.route('/photo/<int:id>/modify/')
def modify_photo(id):
    return u'未完成'


@photo.route('/photo/<int:id>/delete/')
def delete_photo(id):
    """删除照片"""
    photo = Photo.query.get_or_404(id)
    #if photo.people_id != g.user.id:
    #    flash(u'删除失败', 'warning')
    #    return redirect(url_for('show_photo', id=id))
    try:
        os.remove(photos.url(photo.uri))
    except OSError as e:
        pass
    db.session.delete(photo)
    db.session.commit()
    flash(u'删除成功', 'success')
    return redirect(url_for('frontend.album', id=g.user.id))



@photo.route('/photo/<int:pid>/move/<int:aid>/')
def move_to_album(pid, aid):
    pass


@photo.route('/photo/<int:pid>/comment/')
@photo.route('/photo/<int:pid>/comment/<int:cid>/')
def comment_photo(pid, cid):
    pass


@photo.route('/photo/comment/<int:id>/delete/')
def delete_comment(id):
    pass

