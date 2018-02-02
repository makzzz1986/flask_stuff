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
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    comment = db.relationship('Comment', backref='author', lazy='dynamic')
    logs = db.relationship('Logs', backref='specialist', lazy='dynamic')
    azs_added = db.relationship('AZS', backref='specialist', lazy='dynamic')
    about_me = db.Column(db.String(140))
    rank = db.Column(db.Integer, db.ForeignKey('rank.id'))
    division = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    azs_id = db.Column(db.Integer, db.ForeignKey('azs.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    azs_id = db.Column(db.Integer, db.ForeignKey('azs.id'))
    sixdign = db.Column(db.String(6))

    def __repr__(self):
        return '<Log {}>'.format(self.body)

class Divisions(db.Model):
    __tablename__ = 'divisions'
    id = db.Column(db.Integer, primary_key=True)
    div_name = db.Column(db.String(40))
    user = db.relationship('User', backref='otdel', lazy='dynamic')

class Rank(db.Model):
    __tablename__ = 'rank'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    user = db.relationship('User', backref='grade', lazy='dynamic')

class AZS(db.Model):
    __tablename__ = 'azs'
    id = db.Column(db.Integer, primary_key=True)
    sixdign = db.Column(db.String(6), index=True, unique=True)
    ru = db.Column(db.Integer, db.ForeignKey('ru.id'))
    region_mgmt = db.Column(db.Integer, db.ForeignKey('region_mgmt.id'))
    num = db.Column(db.Integer, unique=False)
    hostname = db.Column(db.String(30))
    dzo = db.Column(db.Integer, db.ForeignKey('dzo.id'))
    azs_type = db.Column(db.Integer, db.ForeignKey('azs_type.id'))
    active = db.Column(db.Boolean)
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_added = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.relationship('Status', uselist=False, back_populates='azs')
    address = db.Column(db.String(120))
#    channels = db.relationship('Channels', uselist=False, back_populates='azs')
    hardware = db.relationship('Hardware', uselist=False, back_populates='azs')
    mss_ip = db.Column(db.String(15))
    ip = db.relationship('Ip', backref='author', lazy='dynamic')
    need_to_check = db.Column(db.Boolean)
    comment = db.relationship('Comment', backref='azs', lazy='dynamic')
    logs = db.relationship('Logs', backref='azs', lazy='dynamic')

    def __repr__(self):
        return '<AZS {} with sixdign {}>'.format(self.id, self.sixdign)

class Ip(db.Model):
    __tablename__ = 'ip'
    id = db.Column(db.Integer, primary_key=True)
    interface = db.Column(db.String(10))
    net = db.Column(db.String(35), unique=True)
    description = db.Column(db.String(30))
    renew_last_time = db.Column(db.DateTime, default=datetime.utcnow)
    azs_id = db.Column(db.Integer, db.ForeignKey('azs.id'))

class Hardware(db.Model):
    __tablename__ = 'hardware'
    id = db.Column(db.Integer, primary_key=True)
    gate_model = db.Column(db.Integer, db.ForeignKey('models_gate.id'))
    # gate_vers = db.Column(db.String(10))
    gate_serial = db.Column(db.String(10), unique=True)
    gate_lic = db.Column(db.String(10))
    # gate_owner = db.Column(db.Integer, db.ForeignKey('dzo.id'))
    gate_install = db.Column(db.DateTime, default=datetime.utcnow)
    router_model = db.Column(db.Integer, db.ForeignKey('models_router.id'))
    # router_model = db.Column(db.String(10))
    router_serial = db.Column(db.String(10), unique=True)
    # router_lic = db.Column(db.String(10))
    # router_owner = db.Column(db.Integer, db.ForeignKey('dzo.id'))
    router_install = db.Column(db.DateTime, default=datetime.utcnow)
    # zip_addr = db.Column(db.Integer, db.ForeignKey('zip_addr.id'))
    azs_id = db.Column(db.Integer, db.ForeignKey('azs.id'), nullable=False)
    azs = db.relationship('AZS', back_populates='hardware')

class Models_gate(db.Model):
    __tablename__ = 'models_gate'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    hardware = db.relationship('Hardware', backref='vend_gate', lazy='dynamic')

class Models_router(db.Model):
    __tablename__ = 'models_router'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    hardware = db.relationship('Hardware', backref='vend_rtr', lazy='dynamic')
    
class RU(db.Model):
    __tablename__ = 'ru'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    geo = db.Column(db.String(60))
    azs = db.relationship('AZS', backref='RU', lazy='dynamic')

class Region_mgmt(db.Model):
    __tablename__ = 'region_mgmt'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    azs = db.relationship('AZS', backref='Region', lazy='dynamic')

class DZO(db.Model):
    __tablename__ = 'dzo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    service = db.Column(db.String(60))
    manager = db.Column(db.String(60))
    azs = db.relationship('AZS', backref='DZO', lazy='dynamic')

class AZS_Type(db.Model):
    __tablename__ = 'azs_type'
    id = db.Column(db.Integer, primary_key=True)
    azstype = db.Column(db.String(30))
    azs = db.relationship('AZS', backref='type', lazy='dynamic')

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)    
    active = db.Column(db.Boolean)
    reason = db.Column(db.Integer, db.ForeignKey('reasons.id'))
    # reason = db.relationship('Reason', backref='reason', lazy='dynamic')
    added = db.Column(db.DateTime, default=datetime.utcnow)
    prereason = db.Column(db.Integer, db.ForeignKey('prereasons.id'))
    # prereason = db.relationship('Reason', backref='prereason', lazy='dynamic')
    preadded = db.Column(db.DateTime, default=datetime.utcnow)
    azs_id = db.Column(db.Integer, db.ForeignKey('azs.id'))
    azs = db.relationship('AZS', back_populates='status')

class Reasons(db.Model):
    __tablename__ = 'reasons'
    id = db.Column(db.Integer, primary_key=True)
    reason_name = db.Column(db.String(30))
    status = db.relationship('Status', backref='reasons', lazy='dynamic')

class PreReasons(db.Model):
    __tablename__ = 'prereasons'
    id = db.Column(db.Integer, primary_key=True)
    reason_name = db.Column(db.String(30))
    status = db.relationship('Status', backref='prereasons', lazy='dynamic')
