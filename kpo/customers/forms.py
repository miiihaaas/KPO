from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class RegisterCustomerForm(FlaskForm):
    customer_name = StringField('Naziv', validators=[DataRequired(), Length(min=2, max=75)])
    customer_address = StringField('Adresa', validators=[DataRequired(), Length(min=2, max=75)])
    customer_address_number = StringField('Broj', validators=[DataRequired(), Length(min=1, max=5)])
    customer_zip_code = StringField('Poštanski broj', validators=[DataRequired(), Length(min=5, max=5)])
    customer_city = StringField('Mesto', validators=[DataRequired(), Length(min=2, max=50)])
    customer_state = StringField('Država', validators=[DataRequired(), Length(min=2, max=50)])
    customer_pib = StringField('PIB', validators=[DataRequired(), Length(min=9, max=9)])
    customer_mb = StringField('MB', validators=[DataRequired(), Length(min=8, max=8)])
    customer_jbkjs = StringField('JBKJS', validators=[DataRequired(), Length(min=5, max=5)])
    customer_mail = StringField('Mejl', validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField('Registrujte komitenta')
    
    
    
class EditCustomerForm(FlaskForm):
    customer_name = StringField('Naziv', validators=[DataRequired(), Length(min=2, max=75)])
    customer_address = StringField('Adresa', validators=[DataRequired(), Length(min=2, max=75)])
    customer_address_number = StringField('Broj', validators=[DataRequired(), Length(min=1, max=5)])
    customer_zip_code = StringField('Poštanski broj', validators=[DataRequired(), Length(min=5, max=5)])
    customer_city = StringField('Mesto', validators=[DataRequired(), Length(min=2, max=50)])
    customer_state = StringField('Dršava', validators=[DataRequired(), Length(min=2, max=50)])
    customer_pib = StringField('PIB', validators=[DataRequired(), Length(min=9, max=9)])
    customer_mb = StringField('MB', validators=[DataRequired(), Length(min=8, max=8)])
    customer_jbkjs = StringField('JBKJS', validators=[DataRequired(), Length(min=5, max=5)])
    customer_mail = StringField('Mejl', validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField('Izmenite podatke')