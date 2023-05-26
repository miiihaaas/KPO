from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional, NumberRange
from kpo.models import Bill


choices = [
    '',
    'PDV-RS-10-2-1',
    'PDV-RS-10-2-2',
    'PDV-RS-10-2-3',
    'PDV-RS-10-2-4',
    'PDV-RS-10-2-5-1',
    'PDV-RS-10-2-5-2',
    'PDV-RS-10-2-5-3',
    'PDV-RS-36b-6',
    'PDV-RS-24-1-2',
    'PDV-RS-24-1-3',
    'PDV-RS-24-1-5',
    'PDV-RS-24-1-5a',
    'PDV-RS-24-1-6',
    'PDV-RS-24-1-6a',
    'PDV-RS-24-1-7',
    'PDV-RS-24-1-7a',
    'PDV-RS-24-1-8',
    'PDV-RS-24-1-9',
    'PDV-RS-24-1-10',
    'PDV-RS-24-1-11',
    'PDV-RS-24-1-12',
    'PDV-RS-24-1-13',
    'PDV-RS-24-1-14',
    'PDV-RS-24-1-15',
    'PDV-RS-24-1-16-1',
    'PDV-RS-24-1-16-2',
    'PDV-RS-24-1-16-3',
    'PDV-RS-24-1-16-4',
    'PDV-RS-24-1-16a',
    'PDV-RS-24-1-16b',
    'PDV-RS-24-1-16v',
    'PDV-RS-24-1-16g',
    'PDV-RS-24-1-17',
    'PDV-RS-6a',
    'PDV-RS-11-1-2',
    'PDV-RS-11-1-3',
    'PDV-RS-11-1-4',
    'PDV-RS-11-1-5',
    'PDV-RS-11-3',
    'PDV-RS-12-4',
    'PDV-RS-12-6-1',
    'PDV-RS-12-6-2',
    'PDV-RS-12-6-3',
    'PDV-RS-12-6-4-1',
    'PDV-RS-12-6-4-2',
    'PDV-RS-12-6-4-3',
    'PDV-RS-12-6-4-4',
    'PDV-RS-12-6-4-5',
    'PDV-RS-12-6-5',
    'PDV-RS-12-6-6',
    'PDV-RS-12-6-7-1',
    'PDV-RS-12-6-7-2',
    'PDV-RS-12-6-7-3',
    'PDV-RS-12-6-7-4',
    'PDV-RS-12-6-7-5',
    'PDV-RS-12-6-7-6',
    'PDV-RS-12-6-7-7',
    'PDV-RS-12-6-7-8',
    'PDV-RS-12-6-7-9',
    'PDV-RS-12-6-7-10',
    'PDV-RS-12-6-7-11',
    'PDV-RS-12-6-7-12',
    'PDV-RS-12-6-8',
    'PDV-RS-12-9',
    'PDV-RS-17-4-2',
    'PDV-RS-61',
    'PDV-RS-4-4-2NP',
    'PDV-RS-5-4-2NP',
    'PDV-RS-3NP-ostalo',
    'PDV-RS-17-4-3',
    'PDV-RS-9',
    'PDV-RS-35-7',
    'PDV-RS-3-DZ',
    'PDV-RS-4',
    'PDV-RS-5',
    'PDV-RS-6-1-1 (BN)'
]


class RegisterBillForm(FlaskForm):
    bill_currency = SelectField('Valuta', choices=[('RSD', 'RSD'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('CHF', 'CHF'), ('AUD', 'AUD')])
    # bill_type = SelectField('Tip dokumenta', choices=[('faktura', 'Faktura'), ('avans', 'Avansni račun')])
    bill_customer_id = SelectField('Kupac')
    bill_number = StringField('Broj dokumenta', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = SelectField('PDV kategorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')])
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=choices)
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)])
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)])
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)])
    bill_transaction_date = StringField('Datum prometa')
    bill_due_date = StringField('Datum dospeća')
    bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('Datum slanja fakture', 'Datum slanja fakture'), ('Datum prometa', 'Datum prometa'), ('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')])
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl')
    submit = SubmitField('Dodajte stavke')


class EditBillForm(FlaskForm):
    bill_currency = SelectField('Valuta', choices=[('RSD', 'RSD'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('CHF', 'CHF'), ('AUD', 'AUD')])
    # bill_type = SelectField('Tip dokumenta', choices=[('faktura', 'Faktura'), ('avans', 'Avansni račun')])
    bill_customer_id = SelectField('Kupac')
    bill_number = StringField('Broj dokumenta', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = SelectField('PDV kategorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')])
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=choices)
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)])
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)])
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)])
    bill_transaction_date = StringField('Datum prometa')
    bill_due_date = StringField('Datum dospeća')
    bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('Datum slanja fakture', 'Datum slanja fakture'), ('Datum prometa', 'Datum prometa'), ('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')])
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl')
    submit = SubmitField('Ažurirajte dokument')
    
    
class RegisterAdvanceAccountForm(FlaskForm): #! avansni račun
    bill_currency = SelectField('Valuta', choices=[('RSD', 'RSD'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('CHF', 'CHF'), ('AUD', 'AUD')])
    # bill_type = SelectField('Tip dokumenta', choices=[('faktura', 'Faktura'), ('avans', 'Avansni račun')])
    bill_customer_id = SelectField('Kupac')
    bill_number = StringField('Broj avansnog računa', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = SelectField('PDV kategorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')])
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=choices)
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)])
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)])
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)])
    # bill_transaction_date = StringField('Datum plaćanja') #! ovo nema avans - Simke odlučio
    bill_due_date = StringField('Datum plaćanja')
    bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')])
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl')
    submit = SubmitField('Dodajte stavke')


class EditAdvanceAccountForm(FlaskForm): #! avansni račun
    bill_currency = SelectField('Valuta', choices=[('RSD', 'RSD'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('CHF', 'CHF'), ('AUD', 'AUD')])
    # bill_type = SelectField('Tip dokumenta', choices=[('faktura', 'Faktura'), ('avans', 'Avansni račun')])
    bill_customer_id = SelectField('Kupac')
    bill_number = StringField('Broj avansnog računa', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = SelectField('PDV kategorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')])
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=choices)
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)])
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)])
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)])
    # bill_transaction_date = StringField('Datum plaćanja') #! ovo nema avans - Simke odlučio
    bill_due_date = StringField('Datum plaćanja')
    bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')])
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl -- radi na ovome :)')
    submit = SubmitField('Ažuirajte dokument')
    
    
class RegisterCreditNoteForm(FlaskForm): #! knjižno odobrenje
    bill_currency = StringField('Valuta') #! readonly, jednako sa fakturom
    # bill_type = SelectField('Tip dokumenta', choices=[('knjizno_odobrenje', 'Knjišno odobrenje')]) #! readonly
    bill_customer_id = SelectField('Kupac') #! readonly, jednako sa fakturom
    bill_number = StringField('Broj knjižnog odobrenja', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = StringField('PDV kategorija') #! readonly, jednako sa fakturom
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=choices) #! readonly, jednako sa fakturom
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    # bill_transaction_date = StringField('Datum prometa')
    # bill_due_date = StringField('Datum dospeća') #! ovo ne treba za knjižno odobrenje
    # bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('Datum slanja fakture', 'Datum slanja fakture'), ('Datum prometa', 'Datum prometa'), ('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')]) #! ovo ne treba za knjižno odobrenje
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl')
    submit = SubmitField('Dodajte stavke')


class EditCreditNoteForm(FlaskForm): #! knjižno odobrenje
    bill_currency = StringField('Valuta') #! readonly, jednako sa fakturom
    # bill_type = SelectField('Tip dokumenta', choices=[('knjizno_odobrenje', 'Knjišno odobrenje')]) #! readonly
    bill_customer_id = SelectField('Kupac') #! readonly, jednako sa fakturom
    bill_number = StringField('Broj knjižnog odobrenja', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = StringField('PDV kategorija') #! readonly, jednako sa fakturom
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=choices) #! readonly, jednako sa fakturom
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    # bill_transaction_date = StringField('Datum prometa') #! ovo ne treba za knjižno odobrenje
    # bill_due_date = StringField('Datum dospeća') #! ovo ne treba za knjižno odobrenje
    # bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('Datum slanja fakture', 'Datum slanja fakture'), ('Datum prometa', 'Datum prometa'), ('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')]) #! ovo ne treba za knjižno odobrenje
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl')
    submit = SubmitField('Ažuirajte dokument')


class RegisterDebitNoteForm(FlaskForm): #! knjižno zaduženje
    bill_currency = StringField('Valuta') #! readonly, jednako sa fakturom
    # bill_type = SelectField('Tip dokumenta', choices=[('knjizno_zaduzenje', 'Knjišno zaduženje')]) #! readonly
    bill_customer_id = SelectField('Kupac') #! readonly, jednako sa fakturom
    bill_number = StringField('Broj knjižnog zaduženja', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = StringField('PDV kategorija') #! readonly, jednako sa fakturom
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=choices) #! readonly, jednako sa fakturom
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    # bill_transaction_date = StringField('Datum prometa')
    bill_due_date = StringField('Datum dospeća')
    bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('Datum slanja fakture', 'Datum slanja fakture'), ('Datum prometa', 'Datum prometa'), ('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')])
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl')
    submit = SubmitField('Dodajte stavke')


class EditDebitNoteForm(FlaskForm): #! knjižno zaduženje
    bill_currency = StringField('Valuta') #! readonly, jednako sa fakturom
    # bill_type = SelectField('Tip dokumenta', choices=[('knjizno_zaduzenje', 'Knjišno zaduženje')]) #! readonly
    bill_customer_id = SelectField('Kupac') #! readonly, jednako sa fakturom
    bill_number = StringField('Broj knjižnog zaduženja', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = StringField('PDV kategorija') #! readonly, jednako sa fakturom
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=choices) #! readonly, jednako sa fakturom
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    # bill_transaction_date = StringField('Datum prometa')
    bill_due_date = StringField('Datum dospeća')
    bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('Datum slanja fakture', 'Datum slanja fakture'), ('Datum prometa', 'Datum prometa'), ('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')])
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl')
    submit = SubmitField('Ažurirajte dokument')