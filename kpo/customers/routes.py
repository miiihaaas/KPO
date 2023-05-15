from kpo.models import Customer, Bill
from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from kpo import db, app
from kpo.customers.forms import RegisterCustomerForm, EditCustomerForm


customers = Blueprint('customers', __name__)

@customers.route('/customer_list')
def customer_list():
    customers = Customer.query.filter_by(company_id=current_user.company_id).all()
    bills = Bill.query.filter_by(bill_company_id=current_user.company_id).all()
    print(f'Komitenti: {customers}')
    print(f'Fakture: {bills}')
    table_data = []
    for customer in customers:
        total_price_by_customer = 0
        count_bills_by_customer = 0
        for bill in bills:
            if int(bill.bill_customer_id) == int(customer.id):
                total_price_by_customer += bill.total_price
                count_bills_by_customer += 1
                print(f'Faktura: {bill.total_price} - Komitent: {customer.customer_name}')
                print(f'{customer.id=}, {total_price_by_customer=}')
        table_data.append({'customer_id': f"{customer.id}", 'total_price': f"{total_price_by_customer}", 'count_bills': f"{count_bills_by_customer}"})
    print(f'Table data: {table_data}')
    
    return render_template('customer_list.html', 
                            customers=customers, 
                            table_data=table_data,
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
    customer = Customer.query.get_or_404(customer_id)
    bills = Bill.query.filter_by(bill_customer_id=customer_id).all()
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
    return render_template('customer.html', legend='Komitent',  title='Komitent', form=form, customer=customer, bills=bills)
    
