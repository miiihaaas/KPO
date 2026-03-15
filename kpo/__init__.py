import os
from datetime import date, timedelta
from flask import Flask, render_template, g, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
#kod ispod treba da reši problem Internal Server Error - komunikacija sa serverom
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

@app.errorhandler(401)
def unauthorized(e):
    error_info = "An error occurred: " + str(e)
    return render_template('401.html', error_info=error_info), 401

@app.errorhandler(403)
def forbidden(e):
    error_info = "An error occurred: " + str(e)
    return render_template('403.html', error_info=error_info), 403

@app.errorhandler(404)
def page_not_found(e):
    error_info = "An error occurred: " + str(e)
    return render_template('404.html', error_info=error_info), 404

@app.errorhandler(500)
def internal_server_error(e):
    error_info = "An error occurred: " + str(e)
    return render_template('500.html', error_info=error_info), 500

@app.errorhandler(502)
def bad_gateway(e):
    error_info = "An error occurred: " + str(e)
    return render_template('502.html', error_info=error_info), 502

@app.errorhandler(Exception)
def handle_error(e):
    error_info = "An error occurred: " + str(e)
    return render_template('500.html', error_info=error_info), 500


db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True, render_as_batch=True) #da primeti izmene npr u dužini stringova
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER') # dodati u .env: 'mail.kpo.digital'
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT') # dodati u .env: 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER') # https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer   ////// os.environ.get vs os.getenv
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS') # https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer -- za 2 step verification: https://support.google.com/accounts/answer/185833
mail = Mail(app)

@app.before_request
def check_license():
    g.license_expired = False
    g.license_warning = False
    if current_user.is_authenticated and current_user.authorization != 's_admin':
        company = current_user.user_company
        if company and company.license_expiry:
            today = date.today()
            days_left = (company.license_expiry - today).days
            if days_left < 0:
                g.license_expired = True
            elif days_left <= 7:
                g.license_warning = True
                flash(f'Vaša licenca ističe za {days_left} dana ({company.license_expiry.strftime("%d.%m.%Y.")}). '
                      'Javite se administratoru za produžetak licence.', 'warning')


from kpo.companys.routes import companys
from kpo.invoices.routes import invoices
from kpo.users.routes import users
from kpo.main.routes import main
# from kpo.qr.routes import qr


app.register_blueprint(companys)
app.register_blueprint(invoices)
app.register_blueprint(users)
app.register_blueprint(main)
# app.register_blueprint(qr)
