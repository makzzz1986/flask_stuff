from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    comment = db.relationship('Comment', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    rank = db.relationship('Ranks', backref='specialist', lazy='dynamic')
    division = db.relationship('Division', backref='specialist', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Divisions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    specialists = db.relationship('User', backref='division', lazy='dynamic')

class AZS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sixdign = db.Column(db.Mediumint, index=True, unique=True)
    ru = db.relationship('RU', backref='azs', lazy='dynamic')
    region_mngm = db.relationship('Region_mngm', backref='azs', lazy='dynamic')
    num = db.Column(db.Smallint, unique=True)
    hostname = db.Column(db.String(30))
    dzo = db.relationship('DZO', backref='azs', lazy='dynamic')
    azs_type = db.relationship('AZSType', backref='azs', lazy='dynamic')
    active = db.Bit()
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_added = 



class DZO(db.Model):
    id = db.Column(db.Smallint, primary_key=True)    
    name = db.Column(db.String(30))
    service = db.Column(db.String(60))
    manager = db.Column(db.String(60))

class AZSType(db.Model):
    id = db.Column(db.Bit, primary_key=True)
    azstype = db.Column(db.String(30))

