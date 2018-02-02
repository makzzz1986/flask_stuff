from app import db
from app.models import Logs
from datetime import datetime


def get_region_mgmt(ru):
    if ru == 'SPB':
        return 'Санкт-Петербург'
    elif ru == 'MSK':
        return 'Москва'
    elif ru == 'YAR':
        return 'Ярославль'
    elif ru == 'KRD':
        return 'Краснодар'
    elif ru == 'KMR':
        return 'Кемерово'
    elif ru == 'NSK':
        return 'Новосибирск'
    elif ru == 'OMS':
        return 'Омск'
    elif ru == 'CHL':
        return 'Челябинск'
    elif ru == 'TUM':
        return 'Тюмень'
    elif ru == 'EKB':
        return 'Екатеринбург'

def eth_to_vlan(string): # переводим сабинтерфейсы во вланы ВНИМАНИЕ! интерфейсы с eth1 не учитываются, только цифры после точки!
    return 'Vlan ' + string.split('.')[1]

# записываем запись в лог
# ВАЖНО! коммит делаем не здесь, а после вызова, ибо много коммитов не есть хорошо
def add_log(user, body, azs_id=None, sixdign=None):
    new_one = Logs(
        timestamp=datetime.utcnow(),
        user_id=user,
        body=body)
    print(new_one)
    if azs_id is not None:
        new_one.azs_id=azs_id
    if sixdign is not None:
        new_one.sixdign=sixdign
    db.session.add(new_one)

    