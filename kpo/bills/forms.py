from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional, NumberRange
from kpo.models import Bill


class RegisterBillForm(FlaskForm):
    bill_currency = SelectField('Valuta', choices=[('RSD', 'RSD'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('CHF', 'CHF'), ('AUD', 'AUD')])
    bill_type = SelectField('Tip dokumenta', choices=[('faktura', 'Faktura'), ('avans', 'Avansni račun'), ('knjizno_odobrenje', 'Knjizno odobrenje'), ('knjizno_zaduzenje', 'Knjizno zaduzenje')])
    bill_customer_id = SelectField('Kupac')
    bill_number = StringField('Broj dokumenta', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = SelectField('PDV kategorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')])
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=[('', 'testing')])
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)])
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)])
    bill_transaction_date = StringField('Datum prometa')
    bill_due_date = StringField('Datum dospeća')
    bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('Datum slanja fakture', 'Datum slanja fakture'), ('Datum prometa', 'Datum prometa'), ('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')])
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl -- radi na ovome :)')
    submit = SubmitField('Dodajte dokument')


class EditBillForm(FlaskForm):
    bill_currency = SelectField('Valuta', choices=[('RSD', 'RSD'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('CHF', 'CHF'), ('AUD', 'AUD')])
    bill_type = SelectField('Tip dokumenta', choices=[('faktura', 'Faktura'), ('avans', 'Avansni račun'), ('knjizno_odobrenje', 'Knjizno odobrenje'), ('knjizno_zaduzenje', 'Knjizno zaduzenje')])
    bill_customer_id = SelectField('Kupac')
    bill_number = StringField('Broj dokumenta', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = SelectField('PDV kategorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')])
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=[('', 'testing')])
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)])
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)])
    bill_transaction_date = StringField('Datum prometa')
    bill_due_date = StringField('Datum dospeća')
    bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('Datum slanja fakture', 'Datum slanja fakture'), ('Datum prometa', 'Datum prometa'), ('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')])
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl -- radi na ovome :)')
    submit = SubmitField('ažurirajte dokument')
    
    
class RegisterItemForm(FlaskForm):
    item_id = StringField('Šifra', validators=[Optional(), Length(min=0, max=10)])
    item_name = StringField('Naziv', validators=[DataRequired(), Length(min=1, max=100)])
    item_quantity = DecimalField('Količina', validators=[DataRequired()])
    item_unit = SelectField('Jedinca mere', choices=[('kWh', 'kWh'), ('kom', 'kom'), ('kg', 'kg'), ('km', 'km'), ('g', 'g'), ('m', 'm'), ('l', 'l'), ('t', 't'), ('m2', 'm2'), ('m3', 'm3'), ('min', 'min'), ('h', 'h'), ('d', 'd'), ('M', 'M'), ('god', 'god')])
    item_price = DecimalField('Cena', validators=[DataRequired()])
    item_discount = DecimalField('Popust, %', validators=[Optional(), NumberRange(min=0, max=100, message='Popust mora biti između 0 i 100')])
    #? proračun - iznos popusta
    #? proračun - iznos bez PDVa
    item_tax = SelectField('PDV, %', choices=[(('0', '0'), '10', '10'), ('20', '20'),])
    item_tax_category = SelectField('PDV katgorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')])