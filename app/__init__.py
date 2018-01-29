# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from scheduler_jobs import Get_subnets
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'



from app import routes, models, errors

def check_just_added():
    azses = models.AZS.query.all()
    need_to_commit = False
    for azs in azses:
        if azs.just_added is True:
            # print('>>> Check AZS -', azs.sixdign)
            check_backups = Get_subnets(azs.hostname)
            # в result_checking кладём результат поиска в бекапах
            result_checking = check_backups.get_dict()
            # если что-то нашлось
            if result_checking is not None:
                print(result_checking)
                ips = models.Ip.query.filter_by(azs=azs.sixdign).all()
                # print(ips)
                print('>>> Scheduler: add subnets to new azs')
                # никаких записей про эту азс не нашлось
                if len(ips)==0:
                    for eth in result_checking:
                        new_net = models.Ip(
                            interface=eth,
                            net=result_checking[eth],
                            azs=azs.sixdign,
                            renew_last_time=datetime.utcnow())
                        db.session.add(new_net)
                        need_to_commit = True
                    # апдейт азс, меняем just_added, чтобы не опрашивать их каждый раз
                    # update_azs = models.AZS.query.filter_by(id=azs.sixdign)
                    # update_azs.update({'just_added': False})

                    # db.session.commit()
                    # print('>>> DB commited')
                else:
                    # print('>>> Find old subnets!')
                    # флаг, что требуется закоммитить базу
                    # changed = False
                    for eth in result_checking:
                        for ip in ips:
                            if eth==ip.interface:
                                if result_checking[eth] != ip.net:
                                    print('>>> Scheduler: subnets different!')
                                    update_net = models.Ip.query.filter_by(id=ip.id)
                                    update_net.update({'net': result_checking[eth]})
                                    need_to_commit = True                                    
                                else:
                                    # print('>>> subnets the same!')
                                    pass
                    # if changed is True:
                    #     db.session.commit()
                    #     print('>>> DB commited')
                update_azs = models.AZS.query.filter_by(id=azs.sixdign)
                update_azs.update({'just_added': False})
                need_to_commit = True
            else:
                # print('>>> Hostname not founded 8(')
                pass
        else:
            # print('Not new!')
            pass
    if need_to_commit is True:
        db.session.commit()
        print('>>> Scheduler: DB commited!')
    else:
        print('>>> Scheduler: nothing new!')
        
# шедулер
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()
