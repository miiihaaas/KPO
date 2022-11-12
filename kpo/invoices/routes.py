from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort, send_file
from sqlalchemy import func
from kpo import app, db, bcrypt
from kpo.invoices.forms import  RegistrationInvoiceForm, UpdateInvoiceForm, DashboardData
from kpo.models import Company, Invoice, User
from flask_login import current_user, login_required
from kpo.invoices.pdf_form import create_invoice_report

invoices = Blueprint('invoices', __name__)


@invoices.route("/invoice_list", methods=['GET', 'POST'])
def invoice_list():
    if not current_user.is_authenticated:
        flash('You have to be logged in to access this page', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization != 's_admin' and current_user.authorization != 'c_admin':
        abort(403)
    invoices = Invoice.query.all()
    data = DashboardData(current_user.user_company.id)
    if request.method == 'POST':
        start = request.form.get('start') #prilagoditi promenjive
        end = request.form.get('end') #prilagoditi promenjive
        filtered_invoices = [i for i in Invoice.query.filter(Invoice.company_id==current_user.user_company.id).filter(Invoice.date.between(start, end)).all()]
        
        file_name = f'{current_user.user_company.companyname}.pdf'
        create_invoice_report(start, end, filtered_invoices, file_name)
        path = "static/pdf_forms/" + file_name
        return send_file(path, as_attachment=True)
        return render_template('invoice_list.html', title='Invoices', invoices=invoices, data=data)
    else:
        return render_template('invoice_list.html', title='Invoices', invoices=invoices, data=data)


@invoices.route("/register_i", methods=['GET', 'POST'])
def register_i():
    if current_user.is_authenticated and (current_user.authorization != 'c_admin' and current_user.authorization != 's_admin'):
        return redirect(url_for('main.home'))

    # ovde je bila class DashboardData:

    data = DashboardData(current_user.user_company.id)
    # print(data.last_input.invoice_number)

    form = RegistrationInvoiceForm()
    form.reset()
    if form.validate_on_submit():
        if current_user.authorization == 'c_admin':
            invoice = Invoice(date=form.date.data,
                                invoice_number=form.invoice_number.data,
                                customer=form.customer.data,
                                service=form.service.data,
                                amount=form.amount.data,
                                company_id=current_user.user_company.id,
                                user_id=current_user.id,
                                cancelled=False)
            db.session.add(invoice)
            db.session.commit()
        elif current_user.authorization == 's_admin':
            invoice = Invoice(date=form.date.data,
                                invoice_number=form.invoice_number.data,
                                customer=form.customer.data,
                                service=form.service.data,
                                amount=form.amount.data,
                                company_id=form.company_id.data,
                                user_id=current_user.id,
                                cancelled=False) #form.user_id.data
            db.session.add(invoice)
            db.session.commit()
        flash(f'Faktura: {form.invoice_number.data} has been created successfully!', 'success')
        return redirect(url_for('invoices.invoice_list'))






    return render_template('register_i.html', title='Register New Vehicle', form=form, data=data)



@invoices.route("/invoice/<int:invoice_id>", methods=['GET', 'POST'])
# @login_required
def invoice_profile(invoice_id): #ovo je funkcija za editovanje vozila
    invoice = Invoice.query.get_or_404(invoice_id)

    print(f'{invoice.date=}')
    if not current_user.is_authenticated:
        flash('You have to be logged in to access this page', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization != 's_admin' and current_user.authorization != 'c_admin':
        abort(403)
    elif current_user.authorization == 'c_admin':
        if current_user.user_company.id != invoice.invoice_company.id:
            abort(403)
    print(Company.query.filter_by(id=invoice.company_id).first().id)
    form = UpdateInvoiceForm()
    if form.validate_on_submit():
        invoice.date = form.date.data
        invoice.invoice_number = form.invoice_number.data
        invoice.customer = form.customer.data
        invoice.service = form.service.data
        invoice.amount = form.amount.data
        if current_user.authorization == 'c_admin':
            invoice.company_id = int(current_user.company_id)
            invoice.user_id = int(current_user.id)
        elif current_user.authorization == 's_admin':
            invoice.company_id = form.company_id.data
            invoice.user_id = form.user_id.data
        invoice.cancelled = form.cancelled.data

        db.session.commit()
        flash(f'Invoice {form.invoice_number.data} was updated', 'success')
        return redirect(url_for('invoices.invoice_list'))
    elif request.method == 'GET':
        print(f'{invoice.cancelled=}')
        form.date.data = invoice.date
        form.invoice_number.data = invoice.invoice_number
        form.customer.data = invoice.customer
        form.service.data = invoice.service
        form.amount.data = invoice.amount
        form.company_id.choices = [(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()]
        form.company_id.data = str(invoice.company_id)
        form.user_id.choices = [(u.id, u.name + " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).order_by('name').all()]
        form.user_id.data = str(invoice.user_id)
        form.cancelled.data = invoice.cancelled
    return render_template('invoice.html', title="Edit Invoice", invoice=invoice, form=form, legend='Edit Invoice')


@invoices.route("/invoice/<int:invoice_id>/delete", methods=['POST'])
@login_required
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    print(f'debug - {request.form.get("input_password")}')
    if not bcrypt.check_password_hash(current_user.password, request.form.get("input_password")):
        print('nije dobar password')
        flash('Pogrešna lozinka', 'danger')
        return redirect(url_for('invoices.invoice_list'))
        abort(403)
    else:
        if current_user.authorization == 'c_user':
            abort(403)
        elif current_user.authorization == 'c_admin':
            if current_user.user_company.id != invoice.invoice_company.id:
                abort(403)
            db.session.delete(invoice)
            db.session.commit()
            flash(f'Faktura {invoice.invoice_number} je obrisana', 'success' )
            return redirect(url_for('invoices.invoice_list'))
        else:
            db.session.delete(invoice)
            db.session.commit()
            flash(f'Faktura: {invoice.invoice_number} je obrisana', 'success' )
            return redirect(url_for('invoices.invoice_list'))
