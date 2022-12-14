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
# type: ignore        flash('You have to be logged in to access this page', 'danger')
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
    else:
        return render_template('invoice_list.html', title='Fakture', invoices=invoices, data=data)


@invoices.route("/register_i", methods=['GET', 'POST'])
def register_i():
    if current_user.is_authenticated and (current_user.authorization != 'c_admin' and current_user.authorization != 's_admin'):
        return redirect(url_for('main.home'))

    data = DashboardData(current_user.user_company.id)
    data.last_input = Invoice.query.filter_by(company_id=current_user.user_company.id).filter_by(type='faktura').order_by(Invoice.id.desc()).first()
    customer_list = [i.customer for i in db.session.query(Invoice.customer).distinct()]
    print(customer_list)
    form = RegistrationInvoiceForm()
    form.reset()
    if form.validate_on_submit():
        if current_user.authorization == 'c_admin':
            invoice = Invoice(date=form.date.data,
                                invoice_number=form.invoice_number.data,
                                invoice_number_helper=None,
                                customer=form.customer.data,
                                service=form.service.data,
                                amount=form.amount.data,
                                company_id=current_user.user_company.id,
                                user_id=current_user.id,
                                cancelled=False,
                                international_invoice=form.international_invoice.data,
                                type='faktura')
            db.session.add(invoice)
            db.session.commit()
        elif current_user.authorization == 's_admin':
            invoice = Invoice(date=form.date.data,
                                invoice_number=form.invoice_number.data,
                                invoice_number_helper=None,
                                customer=form.customer.data,
                                service=form.service.data,
                                amount=form.amount.data,
                                company_id=form.company_id.data,
                                user_id=current_user.id,
                                cancelled=False,
                                international_invoice=form.international_invoice.data,
                                type='faktura') #form.user_id.data
            db.session.add(invoice)
            db.session.commit()
        flash(f'Faktura: {form.invoice_number.data} je uspešno kreirana!', 'success')
        return redirect(url_for('invoices.invoice_list'))
    return render_template('register_i.html', legend='Dodavanje nove fakture', title='Dodavanje nove fakture', form=form, data=data, customer_list=customer_list)


@invoices.route("/invoice/<int:invoice_id>/<string:type>/register_n", methods=['GET', 'POST'])
def register_n(invoice_id, type):
    if current_user.is_authenticated and (current_user.authorization != 'c_admin' and current_user.authorization != 's_admin'):
        return redirect(url_for('main.home'))
    invoice = Invoice.query.get_or_404(invoice_id)
    data = DashboardData(current_user.user_company.id)
    form = RegistrationInvoiceForm()
    if type == 'odobrenje':
        form.invoice_number.label.text = 'Broj knjižnog odobrenja'
        form.submit.label.text = 'Dodajte knjižno odobrenje'
        legend = 'Dodavanje knjižnog odobrenja'
        data.last_input = Invoice.query.filter_by(company_id=current_user.user_company.id).filter_by(type='odobrenje').order_by(Invoice.id.desc()).first()
    elif type == 'zaduzenje':
        form.invoice_number.label.text = 'Broj knjižnog zaduženja'
        form.submit.label.text = 'Dodajte knjižno zaduženje'
        legend = 'Dodavanje knjižnog zaduženja'
        data.last_input = Invoice.query.filter_by(company_id=current_user.user_company.id).filter_by(type='zaduženje').order_by(Invoice.id.desc()).first()
    if form.validate_on_submit():
        if current_user.authorization == 'c_admin':
            note = Invoice(date=form.date.data,
                                invoice_number=form.invoice_number.data,
                                invoice_number_helper=invoice.invoice_number,
                                customer=form.customer.data,
                                service=form.service.data,
                                amount=-form.amount.data,
                                company_id=current_user.user_company.id,
                                user_id=current_user.id,
                                cancelled=False,
                                international_invoice=form.international_invoice.data,
                                type='odobrenje')
            invoice.invoice_number_helper = form.invoice_number.data
            if type == 'odobrenje':
                print(f'odobrenje treba da je (-): {note.amount}, {note.type=}')
            elif type == 'zaduzenje':
                note.amount = -note.amount
                note.type = 'zaduženje'
                print(f'zaduženje treba da je (+): {note.amount}, {note.type=}')
            db.session.add(note)
            db.session.commit()
        elif current_user.authorization == 's_admin':
            note = Invoice(date=form.date.data,
                                invoice_number=form.invoice_number.data,
                                invoice_number_helper=invoice.invoice_number,
                                customer=form.customer.data,
                                service=form.service.data,
                                amount=-form.amount.data,
                                company_id=form.company_id.data,
                                user_id=current_user.id,
                                cancelled=False,
                                international_invoice=form.international_invoice.data,
                                type='odobrenje') #form.user_id.data
            invoice.invoice_number_helper = form.invoice_number.data
            if type == 'odobrenje':
                print(f'odobrenje treba da je (-): {note.amount}, {note.type=}')
            elif type == 'zaduzenje':
                note.amount = -note.amount
                note.type = 'zaduženje'
                print(f'zaduženje treba da je (+): {note.amount}, {note.type=}')
            db.session.add(note)
            db.session.commit()
        flash(f'Knjižno odobrenje: {form.invoice_number.data} je uspešno kreirano!', 'success')
        return redirect(url_for('invoices.invoice_list'))
    elif request.method == 'GET':
        form.customer.data = invoice.customer
        form.international_invoice.data = invoice.international_invoice
    return render_template('register_i.html', legend=legend + f' ({invoice.invoice_number})', title=legend, form=form, data=data)


@invoices.route("/invoice/<int:invoice_id>", methods=['GET', 'POST'])
# @login_required
def invoice_profile(invoice_id): #ovo je funkcija za editovanje vozila
    invoice = Invoice.query.get_or_404(invoice_id)

    print(f'{invoice.date=}')
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da bi ste pristupili ovoj stranici.', 'danger')
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
        invoice.international_invoice = form.international_invoice.data

        db.session.commit()
        flash(f'Faktura: {form.invoice_number.data} je ažurirana.', 'success')
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
        form.international_invoice.data=invoice.international_invoice
    
    if invoice.type == 'faktura':
        if invoice.invoice_number_helper:
            legend = 'Uređivanje fakture' + f' ({invoice.invoice_number_helper})'
        else:
            legend = 'Uređivanje fakture'
    elif invoice.type == 'odobrenje':
        legend = 'Uređivanje knjižnog odobrenja' + f' ({invoice.invoice_number_helper})'
        form.invoice_number.label.text = 'Broj knjižnog odobrenja'
    else:
        legend = 'Uređivanje knjižnog zaduženja' + f' ({invoice.invoice_number_helper})'
        form.invoice_number.label.text = 'Broj knjižnog zaduženja'
    
    return render_template('invoice.html', title=legend, invoice=invoice, form=form, legend=legend)


@invoices.route("/invoice/<int:invoice_id>/delete", methods=['POST'])
@login_required
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    print(f'debug - {request.form.get("input_password")}')
    if not bcrypt.check_password_hash(current_user.password, request.form.get("input_password")):
        print('nije dobar password')
        flash('Pogrešna lozinka.', 'danger')
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
