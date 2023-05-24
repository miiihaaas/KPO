from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional, NumberRange
from kpo.models import Bill


class RegisterBillForm(FlaskForm):
    bill_currency = SelectField('Valuta', choices=[('RSD', 'RSD'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('CHF', 'CHF'), ('AUD', 'AUD')])
    # bill_type = SelectField('Tip dokumenta', choices=[('faktura', 'Faktura'), ('avans', 'Avansni račun')])
    bill_customer_id = SelectField('Kupac')
    bill_number = StringField('Broj dokumenta', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = SelectField('PDV kategorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')])
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=[('', 'testing')])
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
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=[('', 'testing')])
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
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=[('', 'testing')])
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)])
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)])
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)])
    bill_transaction_date = StringField('Datum plaćanja')
    # bill_due_date = StringField('Datum dospeća') #! ovo nema avans
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
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=[('', 'testing')])
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)])
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)])
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)])
    bill_transaction_date = StringField('Datum plaćanja')
    # bill_due_date = StringField('Datum dospeća') #! ovo nema avans
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
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=[('', 'testing')]) #! readonly, jednako sa fakturom
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
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=[('', 'testing')]) #! readonly, jednako sa fakturom
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
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=[('', 'testing')]) #! readonly, jednako sa fakturom
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_transaction_date = StringField('Datum prometa')
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
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=[('', 'testing')]) #! readonly, jednako sa fakturom
    bill_decision_number = StringField('Broj odluke', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_contract_number = StringField('Broj ugovora', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_service = StringField('Opis knjiženja', validators=[Optional(), Length(min=0, max=250)])
    bill_purchase_order_number = StringField('Broj narudžbenice / ponude', validators=[Optional(), Length(min=0, max=50)]) #! readonly, jednako sa fakturom
    bill_transaction_date = StringField('Datum prometa')
    bill_due_date = StringField('Datum dospeća')
    bill_tax_calculation_date = SelectField('Datum obračuna PDV-a',  choices=[('Datum slanja fakture', 'Datum slanja fakture'), ('Datum prometa', 'Datum prometa'), ('PDV se obračunava na datum plaćanja', 'PDV se obračunava na datum plaćanja')])
    bill_reference_number = StringField('Poziv na broj', validators=[Optional(), Length(min=0, max=50)])
    bill_model = StringField('Model', validators=[Optional(), Length(min=0, max=50)])
    bill_attachment = StringField('Dodaj fajl')
    submit = SubmitField('Ažurirajte dokument')