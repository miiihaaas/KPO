from kpo import app, db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(20), unique=True, nullable=False)         #Helios, Metalac, Tetrapak, Foka, Papir Print
    company_address = db.Column(db.String(20), unique=False, nullable=False)
    company_address_number = db.Column(db.Integer, nullable=False)
    company_zip_code = db.Column(db.Integer, nullable=False)
    company_city = db.Column(db.String(20), unique=False, nullable=False)
    company_state = db.Column(db.String(20), unique=False, nullable=False)
    company_pib = db.Column(db.Integer, nullable=False)
    company_mb = db.Column(db.Integer, nullable=False)
    company_site = db.Column(db.String(20), unique=True, nullable=False) #vidi imali neki model tipa db.Link()
    company_mail = db.Column(db.String(120), unique=True, nullable=False)
    company_phone = db.Column(db.Integer, nullable=False)
    company_logo = db.Column(db.String(60), nullable=False)
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
    customer_name = db.Column(db.String(70), nullable=False)



class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    invoice_number = db.Column(db.String(7), nullable=False)
    customer = db.Column(db.String(70), nullable=False)
    service = db.Column(db.String(70), nullable=True) #usluga
    amount = db.Column(db.Float, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    cancelled = db.Column(db.Boolean(), default=False, nullable=False)

    def __repr__(self):
        return f"Invoice('{self.id=}', '{self.date=}', '{self.invoice_number=}', '{self.customer=}', '{self.service=}', '{self.amount=}')"



db.create_all()
db.session.commit()
