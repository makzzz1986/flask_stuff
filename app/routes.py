# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddAzsForm, ChangeAzsForm
from app.models import User, AZS, RU, AZS_Type, DZO, Hardware, Status
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
#    user = {'username': 'User'}
    # posts = [
    #      {'author': {'username': 'John'}, 'body': 'First one'},
    #      {'author': {'username': 'Susan'}, 'body': 'Second one'},
    #      {'author': {'username': 'Bob'}, 'body': 'Last one'},
    # ]
    # join_ru = join(azs, ru, azs.ru=azs.id)
    azses = AZS.query.join(RU, AZS.ru==RU.id)
    # print(str(AZS.query.join(RU, AZS.ru==RU.id)))
    # azses = AZS.query.all()
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
    form = AddAzsForm()
    form.ru.choices = [(ru.id, ru.name) for ru in RU.query.all()]
    form.dzo.choices = [(dzo.id, dzo.name) for dzo in DZO.query.all()]
    form.azs_type.choices = [(azstype.id, azstype.azstype) for azstype in AZS_Type.query.all()]
    print('>>> GET')
    if form.validate_on_submit():
        # azs = AZS(sixdign=form.sixdign.data, ru=form.ru.data, region_mgmt=form.managed.data, \
        #     num=form.num.data, hostname=form.hostname.data, dzo=form.dzo.data, azs_type=form.azs_type.data, \
        #     active=form.active.data, address=form.address.data)
        check = AZS.query.filter_by(id=form.sixdign.data).first()
        # print('>>> check:', check)
        # регистрируем под шестизнаком если нет такого id уже
        if check is None:
            # print('>>> None')
            # print(current_user)
            reg_num = str(form.sixdign.data)[:3]
            ru_name = RU.query.filter_by(id=form.ru.data).first()
            hostname_gen = 'AZS-{}-{}-CSP-{}'.format(ru_name.name, reg_num, str(form.num.data))
            azs = AZS(\
                id=form.sixdign.data, \
                sixdign=form.sixdign.data, \
                num=form.num.data, \
                hostname=hostname_gen, \
                active=form.active.data, \
                address=form.address.data, \
                data_added=datetime.utcnow(), \
                user_added=current_user.id, \
                ru=form.ru.data)

            hardware = Hardware(\
                id=form.sixdign.data, \
                azs_id=form.sixdign.data, \
                gate_install=datetime.utcnow(), \
                router_install=datetime.utcnow())

            status = Status(\
                id=form.sixdign.data, \
                azs_id=form.sixdign.data, \
                added=datetime.utcnow())
            if form.active.data is True:
                status.reason=1
                status.active=True
            else:
                status.reason=2
                status.active=False
        else:
            # print('>>> ELSE')
            flash('This AZS ({}) already existed! '.format(str(form.sixdign.data)))
            return redirect(url_for('add_azs'))            

        db.session.add(azs)
        db.session.add(hardware)
        db.session.add(status)
        db.session.commit()
        # flash('Congratulations, you add a new AZS - ' + str(form.sixdign.data))
        flash('Congratulations, you add ' + hostname_gen + '!')
        return redirect(url_for('add_azs'))
    print('>>> Validate:', form.validate_on_submit())
    return render_template('add_azs.html', title='Adding new AZS', form=form)

# @login_required
@app.route('/change_azs', methods=['GET', 'POST'])
def add_azs():
    form = ChangeAzsForm()
    
    # form.sixdign.default=
    form.ru.choices = [(ru.id, ru.name) for ru in RU.query.all()]
    form.dzo.choices = [(dzo.id, dzo.name) for dzo in DZO.query.all()]
    form.azs_type.choices = [(azstype.id, azstype.azstype) for azstype in AZS_Type.query.all()]
    if form.validate_on_submit():
        # azs = AZS(sixdign=form.sixdign.data, ru=form.ru.data, region_mgmt=form.managed.data, \
        #     num=form.num.data, hostname=form.hostname.data, dzo=form.dzo.data, azs_type=form.azs_type.data, \
        #     active=form.active.data, address=form.address.data)
        check = AZS.query.filter_by(id=form.sixdign.data).first()
        # print('>>> check:', check)
        # регистрируем под шестизнаком если нет такого id уже
        if check is None:
            # print('>>> None')
            # print(current_user)
            reg_num = str(form.sixdign.data)[:3]
            ru_name = RU.query.filter_by(id=form.ru.data).first()
            hostname_gen = 'AZS-{}-{}-CSP-{}'.format(ru_name.name, reg_num, str(form.num.data))
            azs = AZS(\
                id=form.sixdign.data, \
                sixdign=form.sixdign.data, \
                num=form.num.data, \
                hostname=hostname_gen, \
                active=form.active.data, \
                address=form.address.data, \
                data_added=datetime.utcnow(), \
                user_added=current_user.id, \
                ru=form.ru.data)

            hardware = Hardware(\
                id=form.sixdign.data, \
                azs_id=form.sixdign.data, \
                gate_install=datetime.utcnow(), \
                router_install=datetime.utcnow())

            status = Status(\
                id=form.sixdign.data, \
                azs_id=form.sixdign.data, \
                added=datetime.utcnow())
            if form.active.data is True:
                status.reason=1
                status.active=True
            else:
                status.reason=2
                status.active=False
        else:
            # print('>>> ELSE')
            flash('This AZS ({}) already existed! '.format(str(form.sixdign.data)))
            return redirect(url_for('add_azs'))            

        db.session.add(azs)
        db.session.add(hardware)
        db.session.add(status)
        db.session.commit()
        # flash('Congratulations, you add a new AZS - ' + str(form.sixdign.data))
        flash('Congratulations, you add ' + hostname_gen + '!')
        return redirect(url_for('add_azs'))
    print('>>> Validate:', form.validate_on_submit())
    return render_template('add_azs.html', title='Adding new AZS', form=form)


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

