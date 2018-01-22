from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddAzsForm(FlaskForm):
    sixdign = IntegerField('SixDigitNumber', validators=[DataRequired(), NumberRange(min=1, max=999999)])
    # ru = IntegerField('RU', validators=[DataRequired(), NumberRange(min=1, max=999)])
    # managed = IntegerField('Managed by', validators=[DataRequired()])
    num = IntegerField('Number', validators=[DataRequired(), NumberRange(min=1, max=999)])
    address = StringField('Address', validators=[DataRequired()])
    hostname = StringField('Hostname', validators=[DataRequired()])
    # dzo = StringField('DZO', validators=[DataRequired()])
    # azs_type = StringField('Type', validators=[DataRequired()])
    # user = SelectField('User', coerce=int)
    user = QuerySelectField(query_factory=lambda:User.query.all(), get_label='username')
    active = BooleanField('Active')
    submit = SubmitField('Add AZS')

    # def edit_user():
    #     user = User.query.all()
    #     print('>>>', user)
    #     form.user.choices = [(1, '1'), (2, '2')]

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
