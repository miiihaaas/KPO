from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from kpo import db
from kpo.models import Company, User


class RegistrationUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) #stavljaće se podrazumevana šifra tipa: korisnik1234
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    workplace = StringField('Workplace', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Authorization Level', validators=[DataRequired()], choices = [('c_user', 'USER'),('c_admin', 'ADMIN')])
    gender = SelectField('Gender', validators=[DataRequired()], choices = [(0, 'SREDNJI'),(1, 'MUŠKI'),(2, 'ŽENSKI')])
    company_id = SelectField('Company ID', choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()]) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    submit = SubmitField('Register User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one')

    def reset(self):
        self.__init__()


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    workplace = StringField(label='Workplace', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Authorization Level', validators=[DataRequired()], choices = [('c_user', 'USER'),('c_admin', 'ADMIN')])
    gender = SelectField('Gender', validators=[DataRequired()], choices=[(0, 'SREDNJI'), (1, 'MUŠKI'), (2, 'ŽENSKI')])
    company_id = SelectField('Company ID', choices = [(c.id, c.companyname)for c in db.session.query(Company.id, Company.companyname).order_by('companyname').all()])
    submit = SubmitField('Update User')

    def reset(self):
        self.__init__()



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You have to ask your admin to create an account.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
