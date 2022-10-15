from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from kpo import db
from kpo.models import Company, User


class RegistrationUserForm(FlaskForm):
    email = StringField('Mejl', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired()]) #stavljaće se podrazumevana šifra tipa: korisnik1234
    name = StringField('Ime', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Prezime', validators=[DataRequired(), Length(min=2, max=20)])
    workplace = StringField('Radno mesto', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Nivo autorizacije', validators=[DataRequired()], choices = [('c_user', 'USER'),('c_admin', 'ADMIN')])
    gender = SelectField('Pol', validators=[DataRequired()], choices = [(0, 'SREDNJI'),(1, 'MUŠKI'),(2, 'ŽENSKI')])
    company_id = SelectField('Kompanija', choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()]) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    submit = SubmitField('Registruj korisnika')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one')

    def reset(self):
        self.__init__()


class UpdateUserForm(FlaskForm):
    email = StringField('Mejl', validators=[DataRequired(), Email()])
    name = StringField('Ime', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Prezime', validators=[DataRequired(), Length(min=2, max=20)])
    workplace = StringField(label='Radno mesto', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Nivo autorizacije', validators=[DataRequired()], choices = [('c_user', 'USER'),('c_admin', 'ADMIN')])
    gender = SelectField('Pol', validators=[DataRequired()], choices=[(0, 'SREDNJI'), (1, 'MUŠKI'), (2, 'ŽENSKI')])
    company_id = SelectField('Kompanija', choices = [(c.id, c.companyname)for c in db.session.query(Company.id, Company.companyname).order_by('companyname').all()])
    submit = SubmitField('Ažuriraj podatke')

    def reset(self):
        self.__init__()



class LoginForm(FlaskForm):
    email = StringField('Mejl', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    remember = BooleanField('Zapamti me')
    submit = SubmitField('Uloguj se')


class RequestResetForm(FlaskForm):
    email = StringField('Mejl', validators=[DataRequired(), Email()])
    submit = SubmitField('Zatraži resetovanje lozinke')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Ne postoji nalog sa tim mejlom. Morate zatražiti od Vašeg administratora da Vam kreira nalog.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Lozinka', validators=[DataRequired()])
    confirm_password = PasswordField('Potvrđena lozinka', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Resetuj Lozinku')
