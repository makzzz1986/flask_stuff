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
