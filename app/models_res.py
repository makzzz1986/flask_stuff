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

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

class Divisions(db.Model):
    __tablename__ = 'divisions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    specialist = db.relationship('User', backref='division', lazy='dynamic')

class Rank(db.Model):
    __tablename__ = 'rank'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    specialist = db.relationship('User', backref='rank', lazy='dynamic')

class AZS(db.Model):
    __tablename__ = 'azs'
    id = db.Column(db.Integer, primary_key=True)
    sixdign = db.Column(db.Integer, index=True, unique=True)
    ru = db.Column(db.Integer, db.ForeignKey('ru.id'))
    region_mgmt = db.Column(db.Integer, db.ForeignKey('region_mgmt.id'))
    num = db.Column(db.Integer, unique=True)
    hostname = db.Column(db.String(30))
    dzo = db.Column(db.Integer, db.ForeignKey('dzo.id'))
    azs_type = db.Column(db.Integer, db.ForeignKey('azs_type.id'))
    active = db.Column(db.Boolean)
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_added = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.relationship('Status', uselist=False, back_populates='azs')
    address = db.Column(db.String(120))
    channels = db.relationship('Channels', uselist=False, back_populates='azs')
    hardware = db.relationship('Hardware', uselist=False, back_populates='azs')
    ip = db.relationship('Ip', uselist=False, back_populates='azs')
    

class Ip(db.Model):
    __tablename__ = 'ip'
    id = db.Column(db.Integer, primary_key=True)
    mss_net = db.Column(db.String(10))
    kspd_all = db.Column(db.String(10))
    s_arm = db.Column(db.String(10))
    s_su = db.Column(db.String(10))
    s_tel = db.Column(db.String(10))
    s_tv = db.Column(db.String(10))
    s_video = db.Column(db.String(10))
    s_kontar = db.Column(db.String(10))
    s_interkom = db.Column(db.String(10))
    x_coffe = db.Column(db.String(10))
    x_kkm = db.Column(db.String(10))
    x_term = db.Column(db.String(10))
    x_safe = db.Column(db.String(10))
    azs_id = db.Column(db.Integer, db.ForeignKey('azs.id'))
    azs = db.relationship('AZS', back_populates='ip')

class Hardware(db.Model):
    __tablename__ = 'hardware'
    id = db.Column(db.Integer, primary_key=True)
    gate_vend = db.Column(db.Integer, db.ForeignKey('vendors_gate.id'))
    gate_vers = db.Column(db.String(10))
    gate_serial = db.Column(db.String(10))
    gate_lic = db.Column(db.String(10))
    gate_owner = db.Column(db.Integer, db.ForeignKey('dzo.id'))
    gate_install = db.Column(db.DateTime, default=datetime.utcnow)
    router_vend = db.Column(db.Integer, db.ForeignKey('vendors_router.id'))
    router_vers = db.Column(db.String(10))
    router_serial = db.Column(db.String(10))
    router_lic = db.Column(db.String(10))
    router_owner = db.Column(db.Integer, db.ForeignKey('dzo.id'))
    router_install = db.Column(db.DateTime, default=datetime.utcnow)
    zip_addr = db.Column(db.Integer, db.ForeignKey('zip_addr.id'))
    azs_id = db.Column(db.Integer, db.ForeignKey('azs.id'))
    azs = db.relationship('AZS', back_populates='hardware')

class Zip_addr(db.Model):
    __tablename__ = 'zip_addr'
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.String(120))
    city = db.Column(db.String(15), index=True)
    address = db.Column(db.String(30), index=True)
    manager = db.Column(db.String(30))
    contact = db.Column(db.String(30))
    hardware = db.relationship('Hardware', backref='zip_addr', lazy='dynamic')

class Geo(db.Model):
    __tablename__ = 'geo'
    id = db.Column(db.Integer, primary_key=True)
    geo = db.Column(db.String(60))
    azs = db.relationship('Hardware', backref='geo', lazy='dynamic')

class Vendors_gate(db.Model):
    __tablename__ = 'vendors_gate'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    hardware = db.relationship('Hardware', backref='vend_gate', lazy='dynamic')

class Vendors_router(db.Model):
    __tablename__ = 'vendors_router'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    hardware = db.relationship('Hardware', backref='vend_rtr', lazy='dynamic')

class Channels(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)

    main_ex = db.Column(db.Boolean)
    main_isp_id = db.Column(db.Integer, db.ForeignKey('isp.id'))
    main_isp = db.relationship('ISP', backref='main_isp')
    main_isp_id = db.Column(db.Integer, db.ForeignKey('media.id'))
    main_type = db.relationship('Media', backref='main_type')

    back_ex = db.Column(db.Boolean)
    back_isp_id = db.Column(db.Integer, db.ForeignKey('isp.id'))
    back_isp = db.relationship('ISP', backref='back_isp')
    back_type_id = db.Column(db.Integer, db.ForeignKey('media.id'))
    back_type = db.relationship('Media', backref='back_type')

#    channelmain = db.relationship('Channel_main', uselist=False, back_populates='channels')
#    channel_back = db.relationship('Channel_back', uselist=False, back_populates='channels') 
    azs_id = db.Column(db.Integer, db.ForeignKey('azs.id'))
    azs = db.relationship('AZS', back_populates='channels')

#class Channel_main(db.Model):
#    __tablename__ = 'channel_main'
#    id = db.Column(db.Integer, primary_key=True)
#    isp = db.Column(db.Integer, db.ForeignKey('isp.id'))
#    media_type = db.Column(db.Integer, db.ForeignKey('media.id'))
#    net = db.Column(db.String(10))
#    gre = db.Column(db.String(10))
#    channels_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
#    channels = db.relationship('Channels', back_populates='channel_main')

#class Channel_back(db.Model):
#    __tablename__ = 'channel_back'
#    id = db.Column(db.Integer, primary_key=True)
#    isp = db.Column(db.Integer, db.ForeignKey('isp.id'))
#    media_type = db.Column(db.Integer, db.ForeignKey('media.id'))
#    net = db.Column(db.String(10))
#    gre = db.Column(db.String(10))
#    channels_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
#    channels = db.relationship('Channels', back_populates='channel_back')

class ISP(db.Model):
    __tablename__ = 'isp'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    phones = db.Column(db.String(30))
    email = db.Column(db.String(30))
    manager = db.Column(db.String(20))
#    channel_main = db.relationship('channel_main', backref='main_isp', lazy='dynamic')
#    channel_back = db.relationship('channel_back', backref='back_isp', lazy='dynamic')


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    media_type = db.Column(db.String(20))
    quality = db.Column(db.String(20))
#    channel_main = db.relationship('channel_main', backref='main_type', lazy='dynamic')
#    channel_back = db.relationship('channel_back', backref='back_type', lazy='dynamic')

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
    azs = db.relationship('AZS', backref='Region_mgmt', lazy='dynamic')

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
    reason_id = db.Column(db.Integer, db.ForeignKey('reasons.id'))
    reason = db.relationship('Reason', backref='reason', lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    prereason_id = db.Column(db.Integer, db.ForeignKey('reasons.id'))
    prereason = db.relationship('Reason', backref='prereason', lazy='dynamic')

    pretimestamp = db.Column(db.DateTime, default=datetime.utcnow)
    azs_id = db.Column(db.Integer, db.ForeignKey('azs.id'))
    azs = db.relationship('AZS', back_populates='status')

class Reasons(db.Model):
    __tablename__ = 'reasons'
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(30))
#    status = db.relationship('Status', backref='reason', lazy='dynamic')


