# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, Response, send_file
import helpers
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddAzsForm, ChangeAzsForm, EditIpForm
from app.models import User, AZS, RU, AZS_Type, DZO, Hardware, Status, Models_gate, Models_router, Region_mgmt, Ip
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from io import BytesIO
import xlsxwriter


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
# @login_required
def index():
    azses = AZS.query.join(RU, AZS.ru==RU.id)
    return render_template('index.html', title='Все АЗС', azses=azses)

# @app.route('/download_ip', methods=['POST'])
# # @login_required
# def download_ip():
#     if request.method == 'POST':
#         ints_azs_chosen = {}
#         for selected in request.form:
#             if '=' in selected:   # здесь выбранные интерфейсы для АЗС вида {'1': 'eth0.12'}
#                 azs, eth = selected.split('=')
#                 if azs in ints_azs_chosen:
#                     ints_azs_chosen[azs].append(eth) # если уже есть интерфейсы для этой азс - добавим новый
#                 else:    
#                     ints_azs_chosen[azs] = [eth] # если нет - создадим список из одного
#         print(ints_azs_chosen)

#         join = db.join(Ip, AZS, AZS.id==Ip.azs_id)
#         select_ints = db.select([Ip.azs_id, Ip.interface, Ip.net]).select_from(join).where(AZS.id.in_(ints_azs_chosen.keys()))
#         for elem in db.session.execute(select_ints):
#             print(elem)

#         return render_template('download_ip.html', title='Загрузка')

@app.route('/select_ints', methods=['POST'])
# @login_required
def select_ints():
    azses = AZS.query.all()
    rus = RU.query.all()
    # ips = Ip.query.all()

    pageType = 'Controller'

    # выбор интерфейсов из списка азс 
    # select ip.interface from ip join azs on azs.id=ip.azs_id where azs.id in (3,4,5,6,7);

    # выбор уникальных из определённого региона   
    # select distinct ip.interface from ip join azs on azs.id=ip.azs_id where azs.ru=3;

    # print(dir(request))
    # print('>>> откуда пришёл?', request.referrer)
    chose = [] # сюда будем складывать ид АЗСок, что нам передали
    ints_ru_chosen = {} # сюда будем складывать выбранные для РУ интерфейсы
    ints_azs_chosen = {} # сюда будем складывать выбранные для АЗС интерфейсы
    ints_ru_clear = [] # здесь будет список для очистки
    download = False # этот флаг показывает, что пользователь хочет скачать xls
    # print('>>> Ints loaded')
    if request.method == 'POST':
        print('>>> POST')
        for selected in request.form:
            # print(selected)
            if selected == 'download':
                download = True
            elif '-' in selected:
                ru, eth = selected.split('-')
                if eth == 'Clear': # нажата кнопка очистки
                    ints_ru_clear.append(ru)
                else:
                    ints_ru_chosen[ru] = eth # здесь выбранные интерфейсы для РУ вида {'1': 'eth0.12'}
            elif '=' in selected:   # здесь выбранные интерфейсы для АЗС вида {'1': 'eth0.12'}
                azs, eth = selected.split('=')
                # print(ints_azs_chosen)
                if azs in ints_azs_chosen:
                    ints_azs_chosen[azs].append(eth) # если уже есть интерфейсы для этой азс - добавим новый
                else:    
                    ints_azs_chosen[azs] = [eth] # если нет - создадим список из одного
            else:
                chose.append(selected) # теперь chose содержит список АЗС.id вида [1,2,5,12]

        # print(ints_azs_chosen)
        # print(ints_ru_chosen)
        # print(chose)
        
        ints_from_chose = []
        join = db.join(Ip, AZS, AZS.id==Ip.azs_id)
        select_ints = db.select([Ip.interface, Ip.azs_id, AZS.ru]).select_from(join).where(AZS.id.in_(chose))
        for elem in db.session.execute(select_ints):
            temp_list = [x for x in elem]
            if (str(temp_list[2]) not in ints_ru_clear) and \
            ((str(temp_list[2]) in ints_ru_chosen) and (ints_ru_chosen[str(temp_list[2])] == str(temp_list[0])) or \
            ((str(temp_list[1]) in ints_azs_chosen) and (str(temp_list[0]) in ints_azs_chosen[str(temp_list[1])]))): # выбран такой интерфейс для региона
                temp_list.append(True) # нашли интерфейс в помеченных
                # print('>>> FIND CHOSEN!')
            else:
                # if (temp_list[2] in ints_azs_chosen) and (ints_azs_chosen[temp_list[2]] == temp_list[0]):
                temp_list.append(False)
            ints_from_chose.append(temp_list)
        ints_from_chose.sort()
        # print(ints_from_chose)
        # интерфейсы выбранных азс вида 
        # [['eth0.5', 48, 2, False], ['eth0.2', 48, 2, False], ['eth0.12', 48, 2, False], 
        # ['eth0.1', 48, 2, False], ['eth0.7', 48, 2, False], ['eth0.6', 48, 2, False], 
        # ['eth0.3', 48, 2, False], ['eth0.5', 69, 1, True], ['eth0.11', 69, 1, False]]

        azses_from_chose = []
        select_azses = db.select([AZS.id, AZS.sixdign, AZS.ru]).where(AZS.id.in_(chose)) 
        # azses_from_chose = [x for x in db.session.execute(select_azses)]
        for elem in db.session.execute(select_azses):
            temp_list = [x for x in elem]
            # if (temp_list[2] in ints_ru_chosen) and ():
            temp_list.append(False)
            azses_from_chose.append(temp_list)
        # здесь теперь расширенный список АЗС, в нём теперь есть ид, код, РУ, отметка выбранного 
        # [[37, '766325', 2, False], [67, '793805', 1, False], [166, '068101', 1, False], [191, '481729', 1, False]]
        # print(azses_from_chose)

        ru_from_chose = {}
        join = db.join(RU, AZS, AZS.ru==RU.id)
        select_uniq_ru =  db.select([AZS.ru, RU.name]).select_from(join).where(AZS.id.in_(chose)).distinct() 
        # ru_from_chose = [x for x in db.session.execute(select_uniq_ru)]
        for elem in db.session.execute(select_uniq_ru):
            ru_from_chose[elem[0]] = elem[1]
        # уникальные РУ вида {2: 'MSK', 1: 'SPB'}
        # print(ru_from_chose)

        uniq_ints_from_ru = {}
        for ru in ru_from_chose:
            l = list(set([x[0] for x in ints_from_chose if x[2]==ru]))
            l.sort()
            uniq_ints_from_ru[ru] = l
        # print(uniq_ints_from_ru)
        # теперь тут есть для каждого РУ свой набор интерфейсов, которые есть в выбранных азс, вида:
        # {1: ['eth0.1', 'eth0.8', 'eth0.10', 'eth0.6', 'eth0.10', 'eth0.6', 'eth0.4', 'eth0.2', 'eth0.5', 
        # 'eth0.12', 'eth0.3', 'eth0.2', 'eth0.8', 'eth0.9'], 2: ['eth0.11', 'eth0.2', 'eth0.12', 'eth0.7', 
        # 'eth0.3', 'eth0.3', 'eth0.12']}

        # если пользователь нажал скачать!
        if download is True:
            to_xls_list = []
            join = db.join(Ip, AZS, AZS.id==Ip.azs_id)
            select_nets = db.select([AZS.id, AZS.sixdign, AZS.num, AZS.ru, AZS.address, Ip.interface, Ip.net, Ip.description]).select_from(join).where(AZS.id.in_(ints_azs_chosen.keys()))
            for elem in db.session.execute(select_nets):
                azs_id, six, num, ru, addr, eth, net, desc = elem
                # elem[0], elem[1], helpers.eth_to_vlan
                for interface in ints_from_chose:
                    # [['eth0.5', 48, 2, False], ['eth0.2', 48, 2, False], ['eth0.12', 48, 2, False], 
                    # смотрим в списке отмеченных интерфейсов, если находим наши - помещаем в список
                    # возможно был способ сделать хитрый запрос SQL, но мне не удалось с ходу, может в будущем
                    if (azs_id == interface[1]) and \
                       (eth == interface[0]) and \
                       (interface[3] is True):
                        to_xls_list.append(
                            {'azs_id': azs_id, 
                            'sixdign': six, 
                            'num': num, 
                            'ru': ru_from_chose[ru], 
                            'addr': addr, 
                            'int':eth, 
                            'desc': desc, 
                            'subnet': net})
                        continue
            to_xls_list = sorted(to_xls_list, key=lambda elem: elem['sixdign']) # сортируем по коду
            print(to_xls_list)
            # [{'azs_id': 127, 'sixdign': '031871', 'num': 871, 'ru': 'KMR', 'addr': 'DIFFERENT_address-031871', 
            # 'int': 'eth0.10', 'desc': 'пояснения', 'subnet': '10.7.252.245/30'},

            # создаём буффер, заполняемый экселем
            output = BytesIO()
            row_counter = 0
            interface_cols = {}
            with xlsxwriter.Workbook(output) as book:
                sheet = book.add_worksheet('Выборка'+ str(datetime.utcnow()).split()[0])
                cell_bold = book.add_format({'bold': True})
                sheet.set_row(0, 30, cell_bold)
                sheet.write_string(0, 0, '№\nп/п')
                sheet.set_column(0, 0, 3)
                sheet.write_string(0, 1, 'Код')
                sheet.set_column(1, 1, 8)
                sheet.write_string(0, 2, '№')
                sheet.set_column(2, 2, 4)
                sheet.write_string(0, 3, 'Отд.')
                sheet.set_column(3, 3, 6)
                sheet.write_string(0, 4, 'Адрес')
                sheet.set_column(4, 4, 24)

                # заполняем строки с данными АЗС
                for azs in to_xls_list:
                    row_counter += 1
                    net_desc = helpers.eth_to_vlan(azs['int'])+'\n'+azs['desc'] # здесь будет номер влана и подпись
                    sheet.write_number(row_counter, 0, row_counter) # номер пункта
                    sheet.write_string(row_counter, 1, azs['sixdign'])      # шестизначный код
                    sheet.write_number(row_counter, 2, azs['num'])      # номер
                    sheet.write_string(row_counter, 3, azs['ru'])      # РУ
                    sheet.write_string(row_counter, 4, azs['addr'])      # адрес

                    if net_desc not in interface_cols.keys(): # если в титуле таблицы нет подсети
                        interface_cols[net_desc] = len(interface_cols)+5
                        sheet.write_string(0, interface_cols[net_desc], net_desc)
                        sheet.set_column(interface_cols[net_desc], interface_cols[net_desc], 16)

                    sheet.write_string(row_counter, interface_cols[net_desc], azs['subnet'])


            output.seek(0)
            return send_file(output, attachment_filename='azs_subnets.xlsx', as_attachment=True)

        # 55, '216977', 'DIFFERENT_address-216977', 'eth0.7', '10.14.249.74/30', None)
        # (55, '216977', 'DIFFERENT_address-216977', 'eth0.8', '10.3.50.94/30', None)

        # print(ints_from_chose)
        # print(ru_from_chose)
        # print(uniq_ints_from_ru)

        # return render_template('select_ints.html', title='Выберите интерфейсы', chose=chose, rus=rus, azses=azses, pageType=pageType)
        return render_template('select_ints.html', title='Выберите интерфейсы', pageType=pageType, rus=ru_from_chose, ints=ints_from_chose, azses=azses_from_chose, ru_ints=uniq_ints_from_ru)


@app.route('/select_azs', methods=['GET', 'POST'])
# @login_required
def select_azs():
    # azses = AZS.query.join(RU, AZS.ru==RU.id)
    azses = AZS.query.all()
    rus = RU.query.all()

    pageType = 'Controller'

    # # print('>>> PAGE RELOADED')
    # if request.method == 'POST':
    #     print('>>> POST')
    #     # print(request.form)
    #     # print(dir(request.form))
    #     s = ''
    #     for select in request.form:
    #         print(select)
    #         s += select + ' '

        # if request.form['lamp'] == 'on':
        # return render_template('select_ints.html', title='Выбраны: '+s, rus=rus, azses=azses, pageType=pageType)
    if request.method == 'GET':
        print('>>> method GET')
        return render_template('select_azs.html', title='Выбор АЗС', rus=rus, azses=azses, pageType=pageType)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# @login_required
@app.route('/add_azs', methods=['GET', 'POST'])
def add_azs():
    form = AddAzsForm(gate=1, router=1)

    form.ru.choices = [(ru.id, ru.name) for ru in RU.query.all()]
    form.dzo.choices = [(dzo.id, dzo.name) for dzo in DZO.query.all()]
    form.gate.choices = [(gate.id, gate.name) for gate in Models_gate.query.all()]
    form.router.choices = [(router.id, router.name) for router in Models_router.query.all()]
    form.azs_type.choices = [(azstype.id, azstype.azstype) for azstype in AZS_Type.query.all()]

    print('>>>', form.is_submitted())
    if form.validate_on_submit():
        check = AZS.query.filter_by(sixdign='%06d' % form.sixdign.data).first()
        # регистрируем под шестизнаком если нет такого id уже
        if check is None:
            reg_num = ('%06d' % form.sixdign.data)[:3]
            ru_name = RU.query.filter_by(id=form.ru.data).first()
            hostname_gen = 'AZS-{}-{}-CSP-{}'.format(ru_name.name, reg_num, str(form.num.data))

            # подбираем дефолтный регион управления
            region_mgmt = Region_mgmt.query.all()
            ru_region = helpers.get_region_mgmt(ru_name.name)
            region_mgmt_chosen = 0
            for one_region in region_mgmt:
                if one_region.name == ru_region:
                    region_mgmt_chosen = one_region.id

            azs = AZS(
                sixdign='%06d' % form.sixdign.data,
                num=form.num.data,
                hostname=hostname_gen,
                active=form.active.data,
                address=form.address.data,
                data_added=datetime.utcnow(),
                user_added=current_user.id,
                ru=form.ru.data,
                region_mgmt=region_mgmt_chosen,
                dzo=form.dzo.data,
                azs_type=form.azs_type.data,
                mss_ip=form.mss_ip.data,
                just_added=True)

            new_azs = AZS.query.filter_by(id=form.sixdign.data).first()

            hardware = Hardware(
                azs_id=new_azs.id, 
                gate_install=datetime.utcnow(), 
                router_install=datetime.utcnow(),
                gate_model=form.gate.data,
                router_model=form.router.data)

            status = Status(
                azs_id=new_azs.id, 
                added=datetime.utcnow())
            if form.active.data is True:
                status.reason=1
                status.active=True
            else:
                status.reason=2
                status.active=False
        else:
            # print('>>> ELSE')
            flash('Код ({}) уже существует! '.format('%06d' % form.sixdign.data))
            return redirect(url_for('add_azs'))            

        db.session.add(azs)
        db.session.add(hardware)
        db.session.add(status)
        db.session.commit()
        # flash('Congratulations, you add a new AZS - ' + str(form.sixdign.data))
        flash('Вы добавили новую АЗС: ' + hostname_gen + '!')
        return redirect(url_for('add_azs'))
    print('>>> Validate:', form.validate_on_submit())
    return render_template('add_azs.html', title='Добавление новой АЗС', form=form)


# @login_required
@app.route('/ip_azs/<id>', methods=['GET', 'POST'])
def ip_azs(id):
    print(request.form)
    azs = AZS.query.filter_by(id=id).first_or_404()
    subnets = Ip.query.filter_by(azs_id=id).all()

    form = EditIpForm()
    azs_title = 'АЗС:{}, {} по адресу {}'.format(azs.sixdign, azs.hostname, azs.address)

    # data = request.form['32']
    print('>>> REQUEST')
    # print(data)
    # form.description.data = 'GHH!'
    if request.method == 'GET':
        return render_template('ip_azs.html', title='Адресация на шлюзе', azs_title=azs_title, subnets=subnets, form=form)
    else:
        print('>>> BEFORE VALIDATE')
        if form.validate_on_submit():
            print('>>> AFTER VALIDATE')  
            pass

# @login_required
# @app.route('/change_azs')
@app.route('/change_azs/<id>', methods=['GET', 'POST'])
def change_azs(id):
    azs = AZS.query.filter_by(id=id).first_or_404()
    hardware = Hardware.query.filter_by(azs_id=id).first_or_404()
    status = Status.query.filter_by(azs_id=id).first_or_404()

    if request.method == 'GET':
        form = ChangeAzsForm(ru=azs.ru, dzo=azs.dzo, azs_type=azs.azs_type, 
            active=azs.active, router_model=hardware.id, gate_model=hardware.id, 
            region_mgmt=azs.region_mgmt)

        form.sixdign.data = azs.sixdign
        form.ru.choices = [(ru.id, ru.name) for ru in RU.query.all()]
        form.dzo.choices = [(dzo.id, dzo.name) for dzo in DZO.query.all()]
        form.azs_type.choices = [(azstype.id, azstype.azstype) for azstype in AZS_Type.query.all()]
        form.region_mgmt.choices = [(region_mgmt.id, region_mgmt.name) for region_mgmt in Region_mgmt.query.all()]

        form.hostname.data = azs.hostname
        form.address.data = azs.address
        form.mss_ip.data = azs.mss_ip
        form.num.data = azs.num

        form.gate_model.choices = [(gate_model.id, gate_model.name) for gate_model in Models_gate.query.all()]
        form.gate_model.data = hardware.gate_model
        form.gate_serial.data = hardware.gate_serial
        form.gate_lic.data = hardware.gate_lic
        form.gate_install.data = hardware.gate_install

        form.router_model.choices = [(router_model.id, router_model.name) for router_model in Models_router.query.all()]
        form.router_model.data = hardware.router_model
        form.router_serial.data = hardware.router_serial
        form.router_install.data = hardware.router_install

    else:
        form = ChangeAzsForm()

        form.ru.choices = [(ru.id, ru.name) for ru in RU.query.all()]
        form.dzo.choices = [(dzo.id, dzo.name) for dzo in DZO.query.all()]
        form.azs_type.choices = [(azstype.id, azstype.azstype) for azstype in AZS_Type.query.all()]
        form.router_model.choices = [(router_model.id, router_model.name) for router_model in Models_router.query.all()]
        form.gate_model.choices = [(gate_model.id, gate_model.name) for gate_model in Models_gate.query.all()]
        form.region_mgmt.choices = [(region_mgmt.id, region_mgmt.name) for region_mgmt in Region_mgmt.query.all()]

        print('>>> BEFORE VALIDATE')
        if form.validate_on_submit():
            print('>>> AFTER VALIDATE')        
            hardware = Hardware.query.filter_by(azs_id=id)
            azs = AZS.query.filter_by(id=id)
            status = Status.query.filter_by(azs_id=id)

            azs.update({
                'num': form.num.data, 
                'hostname': form.hostname.data, 
                'address': form.address.data, 
                'active': form.active.data,
                'mss_ip': form.mss_ip.data,

                'ru': form.ru.data, 
                'dzo': form.dzo.data, 
                'region_mgmt': form.region_mgmt.data, 
                'azs_type': form.azs_type.data, 
                })

            hardware.update({
                'gate_model': form.gate_model.data, 
                'gate_serial': form.gate_serial.data, 
                'gate_lic': form.gate_lic.data, 
                'router_model': form.router_model.data, 
                'router_serial': form.router_serial.data})
            db.session.commit()
            flash('Изменения записаны!')

    return render_template('change_azs.html', title='Изменение параметров АЗС', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Редактирование профиля', form=form)

