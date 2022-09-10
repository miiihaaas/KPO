from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length
from kpo import db
from kpo.models import Company, User


class RegistrationInvoiceForm(FlaskForm):
    date = DateTimeField('Datum: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    invoice_number = StringField('Broj Fakture', validators=[DataRequired(), Length(min=7, max=7)])
    customer = StringField('Kupac', validators=[DataRequired(), Length(min=2, max=50)])
    service = StringField('Usluga', validators=[Length(min=0, max=80)])
    amount = IntegerField('Iznos [din]', validators=[DataRequired()])
    company_id = SelectField('Company ID', choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()])
    user_id = SelectField('User ID', choices=[(u.id, u.name + " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).order_by('name').all()]) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    submit = SubmitField('Dodaj Fakturu')

    def reset(self):
        self.__init__()


class UpdateInvoiceForm(FlaskForm):
    date = DateTimeField('Datum: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    invoice_number = StringField('Broj Fakture', validators=[DataRequired(), Length(min=7, max=7)])
    customer = StringField('Kupac', validators=[DataRequired(), Length(min=2, max=50)])
    service = StringField('Usluga', validators=[Length(min=0, max=50)])
    amount = IntegerField('Iznos [din]', validators=[DataRequired()])
    company_id = SelectField('Company ID', choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()])
    user_id = SelectField('User ID', choices=[(u.id, u.name + " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).order_by('name').all()]) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    cancelled = BooleanField('Storno')
    submit = SubmitField('Izmeni Fakturu')

    def reset(self):
        self.__init__()
