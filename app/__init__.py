# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from scheduler_jobs import Get_subnets

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'



from app import routes, models, errors

def renew_ip():
    azses = models.AZS.query.all()
    for azs in azses:
        print('>>> Check AZS -', azs.sixdign)
        check_backups = Get_subnets(azs.hostname)
        # в result_checking кладём результат поиска в бекапах
        result_checking = check_backups.get_dict()
        # если что-то нашлось
        if result_checking is not None:
            print(result_checking)
            ips = models.Ip.query.filter_by(azs=azs.sixdign).all()
            print(ips)
            # никаких записей про эту азс не нашлось
            if len(ips)==0:
                for eth in result_checking:
                    new_net = models.Ip(
                        interface=eth,
                        net=result_checking[eth],
                        azs=azs.sixdign)
                    db.session.add(new_net)
                # if eth in ips.interface:
                    # print('>>>', eth, ips.interface)
                
                db.session.commit()
                print('>>> DB commited')
            else:
                print('>>> Find old subnets!')


        else:
            print('>>> Hostname not founded 8(')

# шедулер
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
