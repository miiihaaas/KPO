from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField, DateField, IntegerField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Length
from kpo import db
from kpo.models import Company, User, Invoice


class RegistrationInvoiceForm(FlaskForm):
    date = DateField('Datum: ', format='%Y-%m-%d', validators=[DataRequired()])
    invoice_number = StringField('Broj fakture', validators=[DataRequired(), Length(min=1, max=12)])
    customer = StringField('Klijent', validators=[DataRequired(), Length(min=2, max=50)])
    service = StringField('Opis knjiženja', validators=[Length(min=0, max=500)])
    amount = DecimalField('Iznos [din]', validators=[DataRequired()])
    company_id = SelectField('Company ID', choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()])
    user_id = SelectField('User ID', choices=[(u.id, u.name + " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).order_by('name').all()]) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    international_invoice = BooleanField('Ino faktura')
    submit = SubmitField('Dodaj fakturu')

    def reset(self):
        self.__init__()


class UpdateInvoiceForm(FlaskForm):
    date = DateField('Datum: ', format='%Y-%m-%d', validators=[DataRequired()])
    invoice_number = StringField('Broj fakture', validators=[DataRequired(), Length(min=1, max=12)])
    customer = StringField('Klijent', validators=[DataRequired(), Length(min=2, max=50)])
    service = StringField('Opis knjiženja', validators=[Length(min=0, max=500)])
    amount = DecimalField('Iznos [din]', validators=[DataRequired()])
    company_id = SelectField('Company ID', choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()])
    user_id = SelectField('User ID', choices=[(u.id, u.name + " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).order_by('name').all()]) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    cancelled = BooleanField('Storno')
    international_invoice = BooleanField('Ino faktura')
    submit = SubmitField('Ažuriraj')

    def reset(self):
        self.__init__()


class DashboardData():
    def __init__(self, company_id):
        self.company_id = company_id
        self.limit = 6000000
        self.end_day = date.today()
        self.start_day = [date(date.today().year, 1, 1)]
        self.razlika_8m = []
        self.razlika_6m = self.limit - Invoice.query.with_entities(
                            func.sum(Invoice.amount).label("suma")
                            ).filter_by(cancelled=False).filter(Invoice.date.between(self.start_day[0], self.end_day)).filter_by(
                            company_id=self.company_id
                            ).first()[0]
        self.company_id = company_id
        self.last_input = Invoice.query.filter_by(company_id=company_id).order_by(Invoice.id.desc()).first() # dodati filter po preduzeću i porežati silazno --- ovo treba da predstavlja pslednju unetu fakturu
        list = [0, 1, 7, 15, 30, 90] # broj dana za proračun do limita
        for item in list:
            self.start_day.append(date.today() + relativedelta(days=item) + relativedelta(days=-365))
        for value in range(7):
            try:
                self.razlika_8m.append(self.limit + 2000000 - Invoice.query.with_entities(
                            func.sum(Invoice.amount).label("suma")
                            ).filter_by(cancelled=False).filter_by(international_invoice=False).filter(Invoice.date.between(self.start_day[value], self.end_day)).filter_by(
                            company_id=self.company_id
                            ).first()[0])
            except:
                self.razlika_8m.append(0)
