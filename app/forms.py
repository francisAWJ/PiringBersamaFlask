from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Nama Depan', validators=[DataRequired()])
    last_name = StringField('Nama Belakang', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Ulangi password anda', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Daftar')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Mohon gunakan username yang lain.')
    
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Mohon gunakan email yang lain.')

class DonateForm(FlaskForm):
    address = StringField('Alamat', validators=[DataRequired()])
    phone_number = StringField('Nomor Telpon', validators=[DataRequired()])
    food_type = StringField('Jenis Makanan', validators=[DataRequired()])
    portions = IntegerField('Porsi Makanan', validators=[DataRequired()])
    food_desc = StringField('Deskripsi Makanan', validators=[DataRequired()])
    submit = SubmitField('Buat Donasi')
