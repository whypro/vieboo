from flask import Module

photo = Module(__name__, url_prefix='')


@photo.route('/album/<int:id>/')
def show_album(id):
    pass


@photo.route('/album/<int:id>/modify/')
def modify_album(id):
    pass


@photo.route('/album/<int:id>/delete/')
def delete_album(id):
    pass


@photo.route('/album/<int:id>/upload/')
def upload_photo(id):
    pass


@photo.route('/photo/<int:id>/')
def show_photo(id):
    pass


@photo.route('/photo/<int:id>/modify/')
def modify_photo(id):
    pass


@photo.route('/photo/<int:id>/delete/')
def delete_photo(id):
    pass


@photo.route('/photo/<int:pid>/move/<int:aid>/')
def move_to_album(pid, aid):
    pass


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

