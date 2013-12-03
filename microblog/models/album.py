import datetime
from microblog.extensions import db


class PhotoAlbum(db.Model):
    __tablename__ = 'photo_album'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='CASECADE'))


class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    album_id = db.Column(db.Integer)


class VoiceAlbum(db.Model):
    __tablename__ = 'voice_album'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='CASECADE'))


class Voice(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(255))
    description = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    album_id = db.Column(db.Integer)