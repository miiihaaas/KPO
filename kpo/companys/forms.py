from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional
from kpo.models import Company
from kpo.bills.forms import all_posible_base_code_choices
from wtforms import SelectField


class RegistrationCompanyForm(FlaskForm):
    companyname = StringField('Naziv kompanije', validators=[DataRequired(), Length(min=2, max=50)])
    company_address = StringField('Adresa', validators=[DataRequired(), Length(min=2, max=50)])
    company_address_number = StringField('Broj', validators=[DataRequired(), Length(min=1, max=5)])
    company_zip_code = StringField('Poštanski broj', validators=[DataRequired(), Length(min=5, max=5)])
    company_city = StringField('Mesto', validators=[DataRequired(), Length(min=2, max=50)])
    company_state = StringField('Država', validators=[DataRequired(), Length(min=2, max=20)])
    company_pib = StringField('PIB', validators=[DataRequired(), Length(min=5, max=9)]) #koji me min max broj cifara - da li su samo cifre - dali je fiksan broj cifara?
    company_mb = StringField('MB', validators=[DataRequired(), Length(min=5, max=8)])
    company_jbkjs = StringField('JBKJS', validators=[Optional(), Length(min=5, max=5)])
    company_site = StringField('Veb stranica', validators=[DataRequired(), Length(min=5, max=50)])
    company_mail = StringField('Mejl', validators=[DataRequired(), Email()])
    company_phone = StringField('Broj telefona', validators=[DataRequired(), Length(min=9, max=13)])
    company_default_tax_category = SelectField('Podrazumevana PDV kategorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')]) #!
    company_default_base_code = SelectField('Podrazumevana šifra osnova', validators=[Optional()], choices=all_posible_base_code_choices) #!
    company_logo = "" #na ovom poraditi --->> https://www.youtube.com/watch?v=803Ei2Sq-Zs&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=7&ab_channel=CoreySchafer <<--- :)
    submit = SubmitField('Registrujte kompaniju')

    def validate_companyname(self, companyname):
        company = Company.query.filter_by(companyname=companyname.data).first()
        if company:
            # raise ValidationError('That company name is taken, please choose a different one')
            raise ValidationError('Kompanija sa istim imenom je već registrovana, izaberite drugačiji naziv kompanije')

class EditCompanyForm(FlaskForm):
    companyname = StringField('Naziv kompanije', validators=[DataRequired(), Length(min=2, max=50)])
    company_address = StringField('Adresa', validators=[DataRequired(), Length(min=5, max=50)])
    company_address_number = StringField('Broj', validators=[DataRequired(), Length(min=1, max=5)])
    company_zip_code = StringField('Poštanski broj', validators=[DataRequired(), Length(min=5, max=5)])
    company_city = StringField('Mesto', validators=[DataRequired(), Length(min=2, max=50)])
    company_state = StringField('Država', validators=[DataRequired(), Length(min=2, max=20)])
    company_pib = StringField('PIB', validators=[DataRequired(), Length(min=9, max=9)]) #koji me min max broj cifara - da li su samo cifre - dali je fiksan broj cifara?
    company_mb = StringField('MB', validators=[DataRequired(), Length(min=8, max=8)])
    company_jbkjs = StringField('JBKJS', validators=[Optional(), Length(min=5, max=5)])
    company_site = StringField('Veb stranica', validators=[DataRequired(), Length(min=5, max=50)])
    company_mail = StringField('Mejl', validators=[DataRequired(), Email()])
    company_default_tax_category = SelectField('Podrazumevana PDV kategorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')]) #!
    company_default_base_code = SelectField('Podrazumevana šifra osnova', validators=[Optional()], choices=all_posible_base_code_choices) #!
    company_phone = StringField('Broj telefona', validators=[DataRequired(), Length(min=9, max=13)])
    company_logo = FileField('Ažuriranje loga', validators=[FileAllowed(['jpg', 'png'])]) 
    submit = SubmitField('Ažuriraj podatke')
