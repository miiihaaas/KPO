from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional, NumberRange
from kpo.models import Bill


all_posible_base_code_choices = [
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
    
    'PDV-RS-25-1-1a',
    'PDV-RS-25-1-2',
    'PDV-RS-25-1-3',
    'PDV-RS-25-1-4',
    'PDV-RS-25-1-5',
    'PDV-RS-25-1-6',
    'PDV-RS-25-1-7',
    'PDV-RS-25-1-8',
    'PDV-RS-25-2-1',
    'PDV-RS-25-2-2',
    'PDV-RS-25-2-3',
    'PDV-RS-25-2-3a',
    'PDV-RS-25-2-3b',
    'PDV-RS-25-2-5',
    'PDV-RS-25-2-6',
    'PDV-RS-25-2-7',
    'PDV-RS-25-2-8',
    'PDV-RS-25-2-9',
    'PDV-RS-25-2-10',
    'PDV-RS-25-2-11',
    'PDV-RS-25-2-12',
    'PDV-RS-25-2-13',
    'PDV-RS-25-2-14',
    'PDV-RS-25-2-15',
    'PDV-RS-25-2-16',
    'PDV-RS-25-2-17',
    'PDV-RS-25-2-18',
    'PDV-RS-25-2-19',
    
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

    'PDV-RS-4-4-2NP',
    'PDV-RS-5-4-2NP',
    'PDV-RS-3NP-ostalo',
    'PDV-RS-17-4-2',
    'PDV-RS-17-4-3',
    'PDV-RS-9',
    
    'PDV-RS-35-7',
    
    'PDV-RS-3-DZ',
    'PDV-RS-4',
    'PDV-RS-5',
    'PDV-RS-6-1-1 (BN)'
    
]


class Dashboard():
    def __init__(self, company_id):
        self.company_id = company_id
        self.limit = 6000000
        self.end_day = date.today()
        self.start_day = [date(date.today().year, 1, 1)]
        self.razlika_8m = []
        bill_total = Bill.query.with_entities(
                                                func.sum(Bill.total_price).label('total_price')
                                                ).filter_by(bill_status='poslat'
                                                ).filter(Bill.bill_transaction_date.between(self.start_day[0], self.end_day) #! bill_transaction_date vs bill_due_date?
                                                ).filter_by(bill_company_id=self.company_id
                                                ).first()[0]
        if bill_total is not None:
            self.razlika_6m = self.limit - bill_total
        else:
            self.razlika_6m = 0
        list = [0, 1, 7, 15, 30, 90]
        for item in list:
            self.start_day.append(date.today() + relativedelta(days=item) + relativedelta(days=-365))
        for value in range(7):
            try:
                print(f'početni dan: {self.start_day[value]}, krajnji dan {self.end_day}')
                bill_total = Bill.query.with_entities(
                                                    func.sum(Bill.total_price).label('total_price')
                                                    ).filter_by(bill_status='poslat'
                                                    ).filter(Bill.bill_due_date.between(self.start_day[value], self.end_day)
                                                    ).filter_by(bill_company_id=self.company_id
                                                    ).first()[0]
                if bill_total is not None:
                    print(f'{bill_total=}')
                    self.razlika_8m.append(self.limit - bill_total + 2_000_000)
                else:
                    print(f'{bill_total=}')
                    self.razlika_8m.append(0)
            except:
                self.razlika_8m.append(0)


class RegisterBillForm(FlaskForm):
    bill_currency = SelectField('Valuta', choices=[('RSD', 'RSD'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('CHF', 'CHF'), ('AUD', 'AUD')])
    # bill_type = SelectField('Tip dokumenta', choices=[('faktura', 'Faktura'), ('avans', 'Avansni račun')])
    bill_customer_id = SelectField('Kupac')
    bill_number = StringField('Broj dokumenta', validators=[DataRequired(), Length(min=3, max=50)])
    bill_tax_category = SelectField('PDV kategorija', choices=[('S', 'S'), ('AE', 'AE'), ('O', 'O'), ('E', 'E'), ('R', 'R'), ('Z', 'Z'), ('SS', 'SS'), ('OE', 'OE'), ('N', 'N')])
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=all_posible_base_code_choices)
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
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=all_posible_base_code_choices)
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
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=all_posible_base_code_choices)
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
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=all_posible_base_code_choices)
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
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=all_posible_base_code_choices) #! readonly, jednako sa fakturom
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
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=all_posible_base_code_choices) #! readonly, jednako sa fakturom
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
    bill_base_code = SelectField('Šifra osnova', validators=[Optional()], choices=all_posible_base_code_choices) #! readonly, jednako sa fakturom
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
    bill_base_code = SelectField('Šifra Osnova', validators=[Optional()], choices=all_posible_base_code_choices) #! readonly, jednako sa fakturom
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