from datetime import datetime
from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from kpo import db, app
from kpo.models import Bill, Customer
from kpo.bills.forms import RegisterBillForm, EditBillForm


bills = Blueprint('bills', __name__)


@bills.route("/bill_list")
def bill_list():
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    bills = Bill.query.all()
    return render_template('bill_list.html', title='Lista faktura', bills=bills)


@bills.route("/register_b",  methods=['GET', 'POST'])
def register_b():
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    form = RegisterBillForm()
    form.bill_customer_id.choices = [(c.id, c.customer_name) for c in Customer.query.filter_by(company_id=current_user.company_id).all()]
    if form.validate_on_submit():
        bill = Bill(
            bill_currency=form.bill_currency.data,
            bill_type=form.bill_type.data,
            bill_number=form.bill_number.data,
            bill_tax_category=form.bill_tax_category.data,
            bill_base_code = form.bill_base_code.data,
            bill_decision_number = form.bill_decision_number.data,
            bill_contract_number = form.bill_contract_number.data,
            bill_purchase_order_number = form.bill_purchase_order_number.data,
            bill_transaction_date = datetime.strptime(form.bill_transaction_date.data, '%Y-%m-%d'),
            bill_due_date = datetime.strptime(form.bill_due_date.data, '%Y-%m-%d'),
            bill_tax_calculation_date = form.bill_tax_calculation_date.data,
            bill_reference_number = form.bill_reference_number.data,
            bill_model = form.bill_model.data,
            bill_attachment = form.bill_attachment.data,
            bill_customer_id = form.bill_customer_id.data
        )
        db.session.add(bill)
        db.session.commit()
        flash('Uspesno ste dodali novu fakturu!', 'success')
        return redirect(url_for('bills.bill_list'))
    return render_template('register_b.html', title='Registracija nove fakture', form=form)
    
    
@bills.route("/bill/<int:bill_id>", methods=['GET', 'POST'])
def bill_profile(bill_id):
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    bill = Bill.query.get_or_404(bill_id)
    form = EditBillForm()
    form.bill_customer_id.choices = [(c.id, c.customer_name) for c in Customer.query.filter_by(company_id=current_user.company_id).all()]
    if form.validate_on_submit():
        bill.bill_currency = form.bill_currency.data
        bill.bill_type = form.bill_type.data
        bill.bill_number = form.bill_number.data
        bill.bill_tax_category = form.bill_tax_category.data
        bill.bill_base_code = form.bill_base_code.data
        bill.bill_decision_number = form.bill_decision_number.data
        bill.bill_contract_number = form.bill_contract_number.data
        bill.bill_purchase_order_number = form.bill_purchase_order_number.data
        bill.bill_transaction_date = datetime.strptime(form.bill_transaction_date.data, '%Y-%m-%d')
        bill.bill_due_date = datetime.strptime(form.bill_due_date.data, '%Y-%m-%d')
        bill.bill_tax_calculation_date = form.bill_tax_calculation_date.data
        bill.bill_reference_number = form.bill_reference_number.data
        bill.bill_model = form.bill_model.data
        bill.bill_attachment = form.bill_attachment.data
        bill.bill_customer_id = form.bill_customer_id.data
    elif request.method == 'GET':
        form.bill_currency.data = bill.bill_currency
        form.bill_type.data = bill.bill_type
        form.bill_number.data = bill.bill_number
        form.bill_tax_category.data = bill.bill_tax_category
        form.bill_base_code.data = bill.bill_base_code
        form.bill_decision_number.data = bill.bill_decision_number
        form.bill_contract_number.data = bill.bill_contract_number
        form.bill_purchase_order_number.data = bill.bill_purchase_order_number
        form.bill_transaction_date.data = bill.bill_transaction_date.strftime('%Y-%m-%d')
        form.bill_due_date.data = bill.bill_due_date.strftime('%Y-%m-%d')
        form.bill_tax_calculation_date.data = bill.bill_tax_calculation_date
        form.bill_reference_number.data = bill.bill_reference_number
        form.bill_model.data = bill.bill_model
        form.bill_attachment.data = bill.bill_attachment
        form.bill_customer_id.data = bill.bill_customer_id
        
    return render_template('bill.html', title='Detalji fakture', form=form)