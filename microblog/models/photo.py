import datetime
from microblog.extensions import db
from microblog.helpers import render_uri


class PhotoAlbum(db.Model):
    __tablename__ = 'photo_album'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='CASCADE'))

    photos = db.relationship('Photo', backref=db.backref('album'), lazy='dynamic')
    people = db.relationship('People', backref=db.backref('albums', lazy='dynamic'))

    def __init__(self, title, people_id, description=None):
        self.title = title
        self.people_id = people_id
        self.description = description


class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    album_id = db.Column(db.Integer, db.ForeignKey('photo_album.id', ondelete='SET NULL'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='CASCADE'))

    people = db.relationship('People')

    def __init__(self, uri, people_id, description=None, album_id=None):
        self.uri = uri
        self.description = description
        self.album_id = album_id
        self.people_id = people_id

    def get_uri(self):
        return render_uri(self.uri)

#
#class VoiceAlbum(db.Model):
#    __tablename__ = 'voice_album'
#
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(80), nullable=False)
#    description = db.Column(db.Text)
#    people_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='CASECADE'))


#class Voice(db.Model):
#    __tablename__ = 'voice'
#    id = db.Column(db.Integer, primary_key=True)
#    uri = db.Column(db.String(255))
#    description = db.Column(db.Text)
#    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
#    album_id = db.Column(db.Integer)