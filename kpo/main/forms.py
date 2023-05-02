from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange


class SettingsForm(FlaskForm):
    synchronization_with_eFaktura = BooleanField('Sinhronizacija sa sistemom eFaktura', default=False)
    payment_records = BooleanField('Evidencija o uplatama', default=False)
    synchronization_with_CRF = BooleanField('Sinhronizacija sa CRF-om', default=False)
    forward_invoice_to_customer = BooleanField('Direktno prosleđivanje fakture komitentu na mejl', default=False)
    submit = SubmitField('Ažurirajte podešavanja')