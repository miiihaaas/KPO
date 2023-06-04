from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Blueprint
from flask import  render_template, redirect, url_for, flash, request
from sqlalchemy import func
from kpo import db
from kpo.models import Company, Settings, User
from kpo.invoices.forms import DashboardData
from kpo.bills.forms import Dashboard
from kpo.main.forms import SettingsForm, SelectCompanyForm
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        form = SelectCompanyForm()
        companys = Company.query.all()
        form.company_id.choices = [(company.id, company.companyname) for company in companys]
        dashboard = Dashboard(current_user.user_company.id)
        print(f'{current_user.user_company.id=}')
        print(f'{dashboard=}')

        for attr, value in vars(dashboard).items():
            print(f'{attr} = {value}')
        
        user=User.query.get(current_user.id)
        print(f'{form.company_id.choices=}')
        print(f'{user.company_id=}')
        print(f'{user.user_company.companyname=}')
        print(f'{form.company_id.data=}')
        if form.validate_on_submit():
            user.company_id = form.company_id.data
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            print(f'nije validan form')
    else:
        print(f'nije ulogovan niko')
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'info')
        return redirect(url_for('main.about'))
    return render_template('home.html', title='Početna', form=form, dashboard=dashboard)



@main.route("/about")
def about():
    return render_template('about.html', title='O softveru')


@main.route("/settings/<int:company_id>", methods=['GET', 'POST'])
def settings(company_id):
    if current_user.user_company.id != company_id:
        flash(f'Nemate ovlašćenje da podešavate parametre drugih kompanija.', 'danger')
        return redirect(url_for('main.home'))
    global_settings = Settings.query.filter_by(company_id=company_id).first()
    print(f'{global_settings.id=}')
    form = SettingsForm()
    if form.validate_on_submit():
        global_settings.synchronization_with_eFaktura = form.synchronization_with_eFaktura.data
        global_settings.payment_records = form.payment_records.data
        global_settings.synchronization_with_CRF = form.synchronization_with_CRF.data
        global_settings.forward_invoice_to_customer = form.forward_invoice_to_customer.data
        db.session.commit()
        flash(f'Ažurirana su podešavanja.', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.synchronization_with_eFaktura.data = global_settings.synchronization_with_eFaktura
        form.payment_records.data = global_settings.payment_records
        form.synchronization_with_CRF.data = global_settings.synchronization_with_CRF
        form.forward_invoice_to_customer.data = global_settings.forward_invoice_to_customer
    return render_template('settings.html', title='Podešavanja', form=form)
