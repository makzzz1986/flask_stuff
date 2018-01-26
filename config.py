import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')  or 'secretkey'
    HOST = '0.0.0.0'
    PORT = 5000
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:123@127.0.0.1/uzistuff'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JOBS = [
    {
    'id': 'renew_ip',
    'func': 'app:renew_ip',
    'trigger': 'interval',
    'seconds': 10
    }
    ]
