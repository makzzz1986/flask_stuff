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
    azs_added = db.relationship('AZS', backref='specialist', lazy='dynamic')
    about_me = db.Column(db.String(140))
    rank = db.Column(db.Smallint, db.ForeignKey('rank.id'))
    division = db.Column(db.Smallint, db.ForeignKey('divisions.id'))
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
    id = db.Column(db.Smallint, primary_key=True)
    name = db.Column(db.String(40))
    specialist = db.relationship('User', backref='division', lazy='dynamic')

class Rank(db.Model):
    id = db.Column(db.Smallint, primary_key=True)
    name = db.Column(db.String(40))
    specialist = db.relationship('User', backref='rank', lazy='dynamic')

class AZS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sixdign = db.Column(db.Mediumint, index=True, unique=True)
    ru = db.Column(db.Smallint, db.ForeignKey('ru.id'))
    region_mgmt = db.Column(db.Smallint, db.ForeignKey('region_mgmt.id'))
    num = db.Column(db.Smallint, unique=True)
    hostname = db.Column(db.String(30))
    dzo = db.Column(db.Smallint, db.ForeignKey('dzo.id'))
    azs_type = db.Column(db.Smallint, db.ForeignKey('azs_type.id'))
    active = db.Bit()
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_added = db.Column(db.Integer, db.ForeignKey('user.id'))

class RU(db.Model):
    id = db.Column(db.Smallint, primary_key=True)
    name = db.Column(db.String(20))
    geo = db.Column(db.String(60))
    azs = db.relationship('AZS', backref='RU', lazy='dynamic')

class Region_mgmt(db.Model):
    id = db.Column(db.Smallint, primary_key=True)
    name = db.Column(db.String(20))
    azs = db.relationship('AZS', backref='Region_mgmt', lazy='dynamic')

class DZO(db.Model):
    id = db.Column(db.Smallint, primary_key=True)    
    name = db.Column(db.String(30))
    service = db.Column(db.String(60))
    manager = db.Column(db.String(60))
    azs = db.relationship('AZS', backref='DZO', lazy='dynamic')

class AZSType(db.Model):
    id = db.Column(db.Bit, primary_key=True)
    azstype = db.Column(db.String(30))
    azs = db.relationship('AZS', backref='azs_type', lazy='dynamic')


