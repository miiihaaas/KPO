from datetime import date
from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort, send_file
from flask_login import login_required, current_user
from kpo import db
from kpo.bills.functions import bill_list_gen
from kpo.models import Customer, Bill, Settings
from kpo.customers.forms import RegisterCustomerForm, EditCustomerForm


customers = Blueprint('customers', __name__)

@customers.route('/customer_list', methods = ['GET'])
def customer_list():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date is None or end_date is None:
        start_date = date.today().replace(day=1, month=1).isoformat()
        end_date = date.today().isoformat()
    customers = Customer.query.filter_by(company_id=current_user.company_id).all()
    bills = Bill.query.filter(
        Bill.bill_company_id == current_user.company_id,
        Bill.bill_transaction_date.between(start_date, end_date)).all() #! ako bude dileme bill_due_date vs bill_transaction_date
    company_settings = Settings.query.filter_by(company_id=current_user.company_id).first()
    # print(f'Komitenti: {customers}')
    print(f'Fakture: {bills}')
    table_data = []
    for customer in customers:
        total_price_by_customer = 0
        count_bills_by_customer = 0
        total_payments_by_customer = 0
        total_depts_by_customer = 0
        for bill in bills:
            if int(bill.bill_customer_id) == int(customer.id):
                total_price_by_customer += bill.total_price
                count_bills_by_customer += 1
                total_payments_by_customer += bill.total_payments
                if bill.bill_due_date:
                    if bill.bill_due_date < date.today():
                        total_depts_by_customer += bill.total_price - bill.total_payments
        table_data.append({'customer_id': customer.id, 
                            'customer_name': customer.customer_name,
                            'total_price': total_price_by_customer, 
                            'count_bills': count_bills_by_customer,
                            'total_payments': total_payments_by_customer,
                            'saldo': total_price_by_customer - total_payments_by_customer,
                            'total_depts': total_depts_by_customer})
    print(f'Table data: {table_data}')
    
    return render_template('customer_list.html', 
                            customers=customers, 
                            table_data=table_data,
                            company_settings=company_settings,
                            start_date=start_date,
                            end_date=end_date,
                            legend='Komitenti',  
                            title='Komitenti')


@customers.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    form = RegisterCustomerForm()
    if form.validate_on_submit():
        customer = Customer(customer_name=form.customer_name.data,
                            customer_address=form.customer_address.data,
                            customer_address_number=form.customer_address_number.data,
                            customer_zip_code=form.customer_zip_code.data,
                            customer_city=form.customer_city.data,
                            customer_state=form.customer_state.data,
                            customer_pib=form.customer_pib.data,
                            customer_mb=form.customer_mb.data,
                            customer_jbkjs=form.customer_jbkjs.data,
                            customer_mail=form.customer_mail.data,
                            company_id=current_user.company_id)
        db.session.add(customer)
        db.session.commit()
        flash(f'Komitent: {form.customer_name.data} je uspesno registrovan.', 'success')
        return redirect(url_for('customers.customer_list'))
    return render_template('register_customer.html', legend='Registracija novog komitenta',  title='Registracija novog komitenta', form=form)


@customers.route('/customer/<int:customer_id>', methods=['GET', 'POST'])
def customer_profile(customer_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date is None or end_date is None:
        start_date = date.today().replace(day=1, month=1).isoformat()
        end_date = date.today().isoformat()
    customer = Customer.query.get_or_404(customer_id)
    print(f'{start_date=}, {end_date=}')
    bills = Bill.query.filter_by(bill_customer_id=customer_id).filter(
            Bill.bill_transaction_date.between(start_date, end_date)).all()
    # bills = Bill.query.filter(
    #     Bill.bill_company_id == current_user.company_id,
    #     Bill.bill_transaction_date.between(start_date, end_date)).all()
    for bill in bills:
        print(f'Faktura: {bill.bill_number=}')
    company_settings = Settings.query.filter_by(company_id=current_user.company_id).first()
    form = EditCustomerForm()
    if form.validate_on_submit():
        customer.customer_name = form.customer_name.data
        customer.customer_address = form.customer_address.data
        customer.customer_address_number = form.customer_address_number.data
        customer.customer_zip_code = form.customer_zip_code.data
        customer.customer_city = form.customer_city.data
        customer.customer_state = form.customer_state.data
        customer.customer_pib = form.customer_pib.data
        customer.customer_mb = form.customer_mb.data
        customer.customer_jbkjs = form.customer_jbkjs.data
        customer.customer_mail = form.customer_mail.data
        customer.company_id = current_user.company_id
        db.session.commit()
        flash('Podaci komitenta su uspešno izmenjeni.', 'success')
        return redirect(url_for('customers.customer_profile', customer_id=customer.id))
    elif request.method == 'GET':
        form.customer_name.data = customer.customer_name
        form.customer_address.data = customer.customer_address
        form.customer_address_number.data = customer.customer_address_number
        form.customer_zip_code.data = customer.customer_zip_code
        form.customer_city.data = customer.customer_city
        form.customer_state.data = customer.customer_state
        form.customer_pib.data = customer.customer_pib
        form.customer_mb.data = customer.customer_mb
        form.customer_jbkjs.data = customer.customer_jbkjs
        form.customer_mail.data = customer.customer_mail
    return render_template('customer.html', 
                            form=form,
                            company_settings = company_settings, 
                            customer=customer, 
                            bills=bills,
                            start_date=start_date,
                            end_date=end_date,
                            legend='Komitent', 
                            title='Komitent',  )
    
    
@customers.route('/export_report/<int:customer_id>', methods=['GET', 'POST'])
def export_report(customer_id):
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    customer = Customer.query.get_or_404(customer_id)
    bills = Bill.query.filter_by(bill_customer_id=customer_id).filter(
            Bill.bill_transaction_date.between(start_date, end_date)).filter(Bill.bill_status == 'poslat').all()
    notes = Bill.query.filter_by(bill_customer_id=customer_id).filter(
            Bill.bill_creation_date.between(start_date, end_date)).all()
    print(f'{notes=}')
    print(f'{bills=}')
    print(customer.customer_name)
    print(f'{start_date=}, {end_date=}')
    print(f'Fakture: {bills}')
    file = 'static/bills_data/' + bill_list_gen(notes, customer, start_date, end_date)
    return send_file(file, mimetype='application/pdf')
