from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange, Optional
from app.models import User,DZO,AZS_Type


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ChangeAzsForm(FlaskForm):
    sixdign = IntegerField()
    ru = SelectField('', coerce=int, option_widget=None)
    num = IntegerField('', validators=[DataRequired(), NumberRange(min=1, max=999)])
    hostname = StringField('', validators=[DataRequired()])
    address = StringField('', validators=[DataRequired()])
    mss_ip = StringField('', validators=[DataRequired()])
    active = BooleanField()

    dzo = SelectField('', coerce=int)
    azs_type = SelectField('', coerce=int)
    region_mgmt = SelectField('', coerce=int)

    gate_model = SelectField('', coerce=int, option_widget=None)
    gate_serial = StringField('', validators=[Optional()])
    gate_lic = StringField('', validators=[Optional()])
    gate_install = StringField('', validators=[Optional()])

    router_model = SelectField('', coerce=int, option_widget=None)
    router_serial = StringField('', validators=[Optional()])
    router_install = StringField('', validators=[Optional()])

    # active = BooleanField('')
    # reason = StringField('')
    # added = StringField('')
    # prereason = StringField('')
    # preadded = StringField('')

    submit = SubmitField('Применить изменения')


class AddAzsForm(FlaskForm):
    sixdign = IntegerField('', validators=[DataRequired(), NumberRange(min=1, max=999999)])
    num = IntegerField('', validators=[DataRequired(), NumberRange(min=1, max=999)])
    mss_ip = StringField('', validators=[DataRequired()])
    address = StringField('', validators=[DataRequired()])
    dzo = SelectField('', coerce=int)
    azs_type = SelectField('', coerce=int)
    ru = SelectField('', coerce=int, option_widget=None)
    gate = SelectField('', coerce=int, option_widget=None)
    router = SelectField('', coerce=int, option_widget=None)
    active = BooleanField('')
    submit = SubmitField('Добавить АЗС')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
             raise ValidationError('Please use a different email')
