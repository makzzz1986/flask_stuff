from app import db
from app.models import User, AZS, RU, AZS_Type, DZO, Hardware, Status, Models_gate, Models_router, Region_mgmt, Ip, Reasons
from random import randint

u = User(username='John', password_hash='pbkdf2:sha256:50000$JzEe85lG$f0a10c3d079bc7c988adb9779f8cd9df5828f9466e1547dd7e300e9497ef9086')
db.session.add(u)
u = User(username='Alice', password_hash='pbkdf2:sha256:50000$JzEe85lG$f0a10c3d079bc7c988adb9779f8cd9df5828f9466e1547dd7e300e9497ef9086')
db.session.add(u)

db.session.commit()

ru = RU(name='SPB')
db.session.add(ru)
ru = RU(name='MSK')
db.session.add(ru)
ru = RU(name='YAR')
db.session.add(ru)
ru = RU(name='KRD')
db.session.add(ru)
ru = RU(name='KMR')
db.session.add(ru)
ru = RU(name='NSK')
db.session.add(ru)
ru = RU(name='OMS')
db.session.add(ru)
ru = RU(name='CHL')
db.session.add(ru)
ru = RU(name='TUM')
db.session.add(ru)
ru = RU(name='EKB')
db.session.add(ru)

db.session.commit()

reg = Region_mgmt(name='Санкт-Петербург')
db.session.add(reg)
reg = Region_mgmt(name='Москва')
db.session.add(reg)
reg = Region_mgmt(name='Ярославль')
db.session.add(reg)
reg = Region_mgmt(name='Краснодар')
db.session.add(reg)
reg = Region_mgmt(name='Кемерово')
db.session.add(reg)
reg = Region_mgmt(name='Новосибирск')
db.session.add(reg)
reg = Region_mgmt(name='Омск')
db.session.add(reg)
reg = Region_mgmt(name='Челябинск')
db.session.add(reg)
reg = Region_mgmt(name='Тюмень')
db.session.add(reg)
reg = Region_mgmt(name='Урал')
db.session.add(reg)

db.session.commit()

dzo = DZO(name='Главный заказчик', service='Договор от 30.01.18', manager='Петров')
db.session.add(dzo)
dzo = DZO(name='Побочный подрядчик', service='Договор не заключён', manager='Иванов')
db.session.add(dzo)

db.session.commit()

azstype = AZS_Type(azstype='АЗС')
db.session.add(azstype)
azstype = AZS_Type(azstype='ААЗС')
db.session.add(azstype)
azstype = AZS_Type(azstype='Смешанная')
db.session.add(azstype)

db.session.commit()

reason = Reasons(reason_name='В работе')
db.session.add(reason)
reason = Reasons(reason_name='Демонтирована')
db.session.add(reason)
reason = Reasons(reason_name='На реконструкции')
db.session.add(reason)
reason = Reasons(reason_name='Сдана в аренду')
db.session.add(reason)

db.session.commit()

mg = Models_gate(name='CryptoGate X')
db.session.add(mg)
mg = Models_gate(name='CryptoGate V')
db.session.add(mg)
mg = Models_gate(name='CryptoGate Y')
db.session.add(mg)
mg = Models_gate(name='CryptoGate Z')
db.session.add(mg)
mg = Models_gate(name='CryptoGate F')
db.session.add(mg)

db.session.commit()

rg = Models_router(name='Router A')
db.session.add(rg)
rg = Models_router(name='Router B')
db.session.add(rg)
rg = Models_router(name='Router C')
db.session.add(rg)
rg = Models_router(name='Router E')
db.session.add(rg)
rg = Models_router(name='Router F')
db.session.add(rg)

db.session.commit()

counter = 0
for i in range(300):
    sixdign = '%06d' % randint(1, 999999)
    num = sixdign[3:]
    ru = randint(1, 10)
    counter += 1
    boole = True if randint(0,1) == 1 else False
    azs = AZS(id=counter, sixdign=sixdign, ru=ru, num=num, hostname='AZS-'+str(ru)+'-'+str(num)+'-CRYPTO', user_added=randint(1,2), address='DIFFERENT_address-'+sixdign, dzo=randint(1,2), azs_type=randint(1,3), active=boole, mss_ip='10.1.1.'+str(randint(1,254)), just_added=True)
    hw = Hardware(azs_id=counter, router_model=randint(1,5), gate_model=randint(1,5))
    st = Status(azs_id=counter, active=boole, reason=randint(1, 4))
    db.session.add(azs)
    db.session.add(hw)
    db.session.add(st)

db.session.commit()

for i in range(300):
    for y in range(7):
        eth = 'eth0.'+str(randint(1,12))
        net = '10.{}.{}.{}/30'.format(randint(1,50), randint(1,254), randint(1,254))
        ip = Ip(interface=eth, net=net, azs_id=i+1)
        db.session.add(ip)

db.session.commit()
print('Updated!')