from kpo import app, db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    synchronization_with_eFaktura = db.Column(db.Boolean, default=False)
    payment_records = db.Column(db.Boolean, default=False)
    synchronization_with_CRF = db.Column(db.Boolean, default=False) #! za sada nemamo tu opciju
    forward_invoice_to_customer = db.Column(db.Boolean, default=False)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(50), unique=True, nullable=False)
    company_address = db.Column(db.String(50), unique=False, nullable=False)
    company_address_number = db.Column(db.String(5), nullable=False)
    company_zip_code = db.Column(db.Integer, nullable=False)
    company_city = db.Column(db.String(50), unique=False, nullable=False)
    company_state = db.Column(db.String(20), unique=False, nullable=False)
    company_pib = db.Column(db.Integer, nullable=False)
    company_mb = db.Column(db.Integer, nullable=False)
    company_jbkjs = db.Column(db.Integer, nullable=True)
    company_site = db.Column(db.String(120), unique=True, nullable=False) #vidi imali neki model tipa db.Link()
    company_mail = db.Column(db.String(120), unique=True, nullable=False)
    company_phone = db.Column(db.String(20), nullable=False)
    company_logo = db.Column(db.String(60), nullable=False)
    dinar_account_list = db.Column(db.JSON, nullable=True)
    foreign_account_list = db.Column(db.JSON, nullable=True)
    users = db.relationship('User', backref='user_company', lazy=True)
    invoices = db.relationship('Invoice', backref='invoice_company', lazy=True)

    def __repr__(self):
        return self.companyname



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable = False)
    name = db.Column(db.String(20), unique=False, nullable=False)
    surname = db.Column(db.String(20), unique=False, nullable=False)
    workplace = db.Column(db.String(20), unique=False, nullable=False)
    authorization = db.Column(db.String(20), nullable = False) # ovde treba da budu tipovi korisnika: S_admin, C_admin, C_user
    gender = db.Column(db.String(1)) #(0, "srednji"), (1, "muški"), (2, "ženski")
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    invoices = db.relationship('Invoice', backref='invoice_user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"{self.id}, '{self.name} {self.surname}'"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(75), nullable=False)
    customer_address = db.Column(db.String(75), unique=False, nullable=False)
    customer_address_number = db.Column(db.String(5), nullable=False)
    customer_zip_code = db.Column(db.Integer, nullable=False)
    customer_city = db.Column(db.String(50), unique=False, nullable=False)
    customer_state = db.Column(db.String(50), unique=False, nullable=False)
    customer_pib = db.Column(db.Integer, nullable=False)
    customer_mb = db.Column(db.Integer, nullable=False)
    customer_jbkjs = db.Column(db.Integer, nullable=False)
    customer_mail = db.Column(db.String(50), unique=False, nullable=False)
    bills = db.relationship('Bill', backref='bill_customer', lazy=True)
    



class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    invoice_number = db.Column(db.String(12), nullable=False)
    invoice_number_helper = db.Column(db.String(12), nullable=True) #! služi za povezivanje knjižnog odobrenja sa brojem fakture
    customer = db.Column(db.String(70), nullable=False)
    service = db.Column(db.String(400), nullable=True) #usluga
    amount = db.Column(db.Float, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    cancelled = db.Column(db.Boolean(), default=False, nullable=False)
    international_invoice = db.Column(db.Boolean(), default=False, nullable=False)
    type = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f"Invoice('{self.id=}', '{self.date=}', '{self.invoice_number=}', '{self.customer=}', '{self.service=}', '{self.amount=}')"
    
    
class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_currency = db.Column(db.String(3), nullable=False)
    bill_type = db.Column(db.String(20), nullable=False)
    bill_number = db.Column(db.String(50), nullable=False)
    bill_tax_category = db.Column(db.String(20), nullable=False)
    bill_base_code = db.Column(db.String(20), nullable=False)
    bill_decision_number = db.Column(db.String(20), nullable=True)
    bill_contract_number = db.Column(db.String(50), nullable=True)
    bill_purchase_order_number = db.Column(db.String(50), nullable=True)
    bill_transaction_date = db.Column(db.Date, nullable=False)
    bill_due_date = db.Column(db.Date, nullable=False)
    bill_tax_calculation_date = db.Column(db.String(35), nullable=True)
    bill_reference_number = db.Column(db.String(50), nullable=True)
    bill_model = db.Column(db.String(50), nullable=True)
    bill_attachment = db.Column(db.String(60), nullable=True)
    bill_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(10), nullable=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_quantity = db.Column(db.Float, nullable=False)
    item_unit = db.Column(db.String(20), nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    item_discount = db.Column(db.Float, nullable=True)
    #? proračun - iznos popusta
    #? proračun - iznos bez PDVa
    item_tax = db.Column(db.Float, nullable=True)
    item_tax_category = db.Column(db.String(2), nullable=False)

db.create_all()
db.session.commit()
