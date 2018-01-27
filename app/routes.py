# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
import helpers
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddAzsForm, ChangeAzsForm, EditIpForm
from app.models import User, AZS, RU, AZS_Type, DZO, Hardware, Status, Models_gate, Models_router, Region_mgmt, Ip
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime


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
    return render_template('index.html', title='Home', azses=azses)

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
    return render_template('login.html', title='Sign In', form=form)

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
        check = AZS.query.filter_by(id=form.sixdign.data).first()
        # регистрируем под шестизнаком если нет такого id уже
        if check is None:
            reg_num = str(form.sixdign.data)[:3]
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
                id=form.sixdign.data,
                sixdign=form.sixdign.data,
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

            hardware = Hardware(
                id=form.sixdign.data, 
                azs_id=form.sixdign.data, 
                gate_install=datetime.utcnow(), 
                router_install=datetime.utcnow(),
                gate_model=form.gate.data,
                router_model=form.router.data)

            status = Status(
                id=form.sixdign.data, 
                azs_id=form.sixdign.data, 
                added=datetime.utcnow())
            if form.active.data is True:
                status.reason=1
                status.active=True
            else:
                status.reason=2
                status.active=False
        else:
            # print('>>> ELSE')
            flash('Код ({}) уже существует! '.format(str(form.sixdign.data)))
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
@app.route('/ip_azs/<sixdign>', methods=['GET', 'POST'])
def ip_azs(sixdign):
    print(request.form)
    azs = AZS.query.filter_by(id=sixdign).first_or_404()
    subnets = Ip.query.filter_by(azs=sixdign).all()

    form = EditIpForm()
    azs_title = 'АЗС:{}, {} по адресу {}'.format(sixdign, azs.hostname, azs.address)

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
@app.route('/change_azs/<sixdign>', methods=['GET', 'POST'])
def change_azs(sixdign):
    azs = AZS.query.filter_by(id=int(sixdign)).first_or_404()
    hardware = Hardware.query.filter_by(id=int(sixdign)).first_or_404()
    status = Status.query.filter_by(id=int(sixdign)).first_or_404()

    if request.method == 'GET':
        form = ChangeAzsForm(ru=azs.ru, dzo=azs.dzo, azs_type=azs.azs_type, 
            active=azs.active, router_model=hardware.id, gate_model=hardware.id, 
            region_mgmt=azs.region_mgmt)

        form.sixdign.data = sixdign
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
            hardware = Hardware.query.filter_by(id=int(sixdign))
            azs = AZS.query.filter_by(id=int(sixdign))
            status = Status.query.filter_by(id=int(sixdign))

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
    return render_template('register.html', title='Register', form=form)

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
    return render_template('edit_profile.html', title='Edit Profile', form=form)

