from datetime import datetime, date
from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from kpo import db, app
from kpo.models import Bill, Customer, Settings, Company
from kpo.bills.forms import RegisterBillForm, EditBillForm, RegisterAdvanceAccountForm, EditAdvanceAccountForm, RegisterCreditNoteForm, EditCreditNoteForm, RegisterDebitNoteForm, EditDebitNoteForm
from kpo.bills.functions import pdf_gen


bills = Blueprint('bills', __name__)


@bills.route("/bill_list")
def bill_list():
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    bills = Bill.query.filter_by(bill_company_id=current_user.company_id).all()
    return render_template('bill_list.html', title='Lista faktura', bills=bills)


@bills.route("/register_b/<string:type>",  methods=['GET', 'POST'])
def register_b(type):
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    if type == 'faktura':
        form = RegisterBillForm()
        title = 'Registracija nove fakture'
        last_document = Bill.query.filter_by(bill_company_id=current_user.company_id).filter_by(bill_type='Faktura').order_by(Bill.bill_number.desc()).first()
    elif type == 'avans':
        form = RegisterAdvanceAccountForm() #todo prilagodi posebnu formu za avans
        title = 'Registracija novog avansnog računa'
        last_document = Bill.query.filter_by(bill_company_id=current_user.company_id).filter_by(bill_type='Avansni račun').order_by(Bill.bill_number.desc()).first()
    dinar_accounts = Company.query.filter_by(id=current_user.user_company.id).first().dinar_account_list
    foreign_accounts = Company.query.filter_by(id=current_user.user_company.id).first().foreign_account_list
    print(f'{dinar_accounts=}')
    print(f'{foreign_accounts=}')
    form.bill_customer_id.choices = [(c.id, c.customer_name) for c in Customer.query.filter_by(company_id=current_user.company_id).all()]
    form.bill_tax_category.data = current_user.user_company.company_default_tax_category
    form.bill_base_code.data = current_user.user_company.company_default_base_code
    if form.validate_on_submit():
        bill_type = 'Faktura' if type == 'faktura' else 'Avansni račun'
        bill = Bill(
            bill_currency = form.bill_currency.data,
            bill_type = bill_type,
            bill_number = form.bill_number.data,
            bill_tax_category = form.bill_tax_category.data,
            bill_base_code = form.bill_base_code.data,
            bill_decision_number = form.bill_decision_number.data,
            bill_contract_number = form.bill_contract_number.data,
            bill_purchase_order_number = form.bill_purchase_order_number.data,
            bill_transaction_date = datetime.strptime(form.bill_transaction_date.data, '%Y-%m-%d') if type == 'faktura' else None,
            bill_due_date = datetime.strptime(form.bill_due_date.data, '%Y-%m-%d'),
            bill_tax_calculation_date = form.bill_tax_calculation_date.data,
            bill_reference_number = form.bill_reference_number.data,
            bill_model = form.bill_model.data,
            bill_original = '',
            bill_attachment = form.bill_attachment.data,
            bill_customer_id = form.bill_customer_id.data,
            bill_company_id = current_user.company_id,
            bill_items = [{'sifra': '', 'naziv': '', 'kolicina': '0', 'jedinica_mere': '', 'cena': '0', 'popust': '0'}],
            bill_payments = [{'payment_date': '', 'payment_amount': ''}],
            bill_status = 'nacrt',
            bill_company_account = request.form['bill_company_account']
        )
        db.session.add(bill)
        db.session.commit()
        return redirect(url_for('bills.bill_profile', bill_id=bill.id))
    return render_template('register_b.html', title=title, form=form, type=type, last_document=last_document, dinar_accounts=dinar_accounts, foreign_accounts=foreign_accounts)


@bills.route("/register_notes/<int:bill_id>/<string:note_type>", methods=['GET', 'POST'])
def register_notes(bill_id, note_type):
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    bill = Bill.query.get_or_404(bill_id)
    if note_type == 'credit_note':
        print('knjižno odobrenje')
        form = RegisterCreditNoteForm()
        title = f'Registracija knjižnog odobrenja za fakturu {bill.bill_number}'
        last_document = Bill.query.filter_by(bill_company_id=current_user.company_id).filter_by(bill_type='Knjižno odobrenje').order_by(Bill.bill_number.desc()).first()
    elif note_type == 'debit_note':
        print('knjižno zaduženje')
        form = RegisterDebitNoteForm()
        title = f'Registracija knjižnog zaduženja za fakturu {bill.bill_number}'
        last_document = Bill.query.filter_by(bill_company_id=current_user.company_id).filter_by(bill_type='Knjižno zaduženje').order_by(Bill.bill_number.desc()).first()
    c = Customer.query.get_or_404(bill.bill_customer_id)
    form.bill_customer_id.choices = [(c.id, c.customer_name)]
    if form.validate_on_submit():
        note = Bill(
            bill_currency=form.bill_currency.data,
            bill_type=form.bill_type.data,
            bill_number=form.bill_number.data,
            bill_tax_category=form.bill_tax_category.data,
            bill_base_code = form.bill_base_code.data,
            bill_decision_number = form.bill_decision_number.data,
            bill_contract_number = form.bill_contract_number.data,
            bill_purchase_order_number = form.bill_purchase_order_number.data,
            bill_due_date = datetime.strptime(form.bill_due_date.data, '%Y-%m-%d'),
            bill_tax_calculation_date = form.bill_tax_calculation_date.data,
            bill_reference_number = form.bill_reference_number.data,
            bill_model = form.bill_model.data,
            bill_original = bill.bill_number, #!
            bill_attachment = form.bill_attachment.data,
            bill_customer_id = form.bill_customer_id.data,
            bill_company_id = current_user.company_id,
            bill_items = [{'sifra': '', 'naziv': '', 'kolicina': '', 'jedinica_mere': '', 'cena': '', 'popust': '0'}],
            bill_payments = [{'payment_date': '', 'payment_amount': ''}],
            bill_status = 'nacrt'
        )
        bill.bill_original = bill.bill_original + f' {note.bill_number}'
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('bills.bill_profile', bill_id=note.id))
    elif request.method == "GET":
        form.bill_currency.data = bill.bill_currency
        form.bill_number.data = ''
        form.bill_tax_category.data = bill.bill_tax_category
        form.bill_base_code.data = bill.bill_base_code
        form.bill_decision_number.data = bill.bill_decision_number
        form.bill_contract_number.data = bill.bill_contract_number
        form.bill_service.data = ''
        form.bill_purchase_order_number.data = bill.bill_purchase_order_number
        if note_type == 'debit_note':
            form.bill_due_date.data = bill.bill_due_date.strftime('%Y-%m-%d')
            form.bill_tax_calculation_date.data = bill.bill_tax_calculation_date
        form.bill_reference_number.data = bill.bill_reference_number
        form.bill_model.data = bill.bill_model
        form.bill_attachment.data = bill.bill_attachment
        form.bill_customer_id.data = str(bill.bill_customer_id)
    return render_template('register_notes.html', title=title, form=form, bill=bill, note_type=note_type, last_document=last_document)



@bills.route("/bill/<int:bill_id>", methods=['GET', 'POST'])
def bill_profile(bill_id):
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    bill = Bill.query.get_or_404(bill_id)
    company_settings = Settings.query.filter_by(company_id=current_user.company_id).first()
    print(f'{bill.bill_type=}')
    if bill.bill_type == 'Knjižno odobrenje':
        form = EditCreditNoteForm()
        c = Customer.query.get_or_404(bill.bill_customer_id)
        form.bill_customer_id.choices = [(c.id, c.customer_name)]
        title = f'Detalji knjižnog odobrenja za fakturu {bill.bill_original}'
    elif bill.bill_type == 'Knjižno zaduženje':
        form = EditDebitNoteForm()
        c = Customer.query.get_or_404(bill.bill_customer_id)
        form.bill_customer_id.choices = [(c.id, c.customer_name)]
        title = f'Detalji knjižnog zaduženja za fakturu {bill.bill_original}'
    elif bill.bill_type == 'Faktura':
        form = EditBillForm()
        form.bill_customer_id.choices = [(c.id, c.customer_name) for c in Customer.query.filter_by(company_id=current_user.company_id).all()]
        title = f'Detalji fakture {bill.bill_number}'
    elif bill.bill_type == 'Avansni račun':
        form = EditAdvanceAccountForm()
        form.bill_customer_id.choices = [(c.id, c.customer_name) for c in Customer.query.filter_by(company_id=current_user.company_id).all()]
        title = f'Detalji avansnog računa {bill.bill_number}'
    dinar_accounts = Company.query.filter_by(id=current_user.user_company.id).first().dinar_account_list
    foreign_accounts = Company.query.filter_by(id=current_user.user_company.id).first().foreign_account_list
    print(f'{bill.bill_company_account=}')
    units = [('kWh', 'kWh'), ('kom', 'kom'), ('kg', 'kg'), ('km', 'km'), ('g', 'g'), ('m', 'metar'), ('l', 'litar'), ('t', 'tona'), ('m2', 'm2'), ('m3', 'm3'), ('min', 'min'), ('h', 'sat'), ('d', 'dan'), ('M', 'mesec'), ('god', 'godina')]
    taxes = [('0', '0%'), ('10', '10%'), ('20', '20%')]
    if form.validate_on_submit():
        bill.bill_currency = form.bill_currency.data
        bill.bill_number = form.bill_number.data
        bill.bill_tax_category = form.bill_tax_category.data
        bill.bill_base_code = form.bill_base_code.data
        bill.bill_decision_number = form.bill_decision_number.data
        bill.bill_contract_number = form.bill_contract_number.data
        bill.bill_service = form.bill_service.data
        bill.bill_purchase_order_number = form.bill_purchase_order_number.data
        bill.bill_transaction_date = datetime.strptime(form.bill_transaction_date.data, '%Y-%m-%d') if  bill.bill_type in ['Faktura'] else None
        bill.bill_due_date = datetime.strptime(form.bill_due_date.data, '%Y-%m-%d') if not bill.bill_type in ['Knjižno odobrenje'] else None
        bill.bill_tax_calculation_date = form.bill_tax_calculation_date.data if not bill.bill_type in ['Knjižno odobrenje'] else None
        bill.bill_reference_number = form.bill_reference_number.data
        bill.bill_model = form.bill_model.data
        bill.bill_attachment = form.bill_attachment.data
        bill.bill_customer_id = form.bill_customer_id.data
        bill.bill_company_account = request.form.get('bill_company_account')
        
        fullname = request.form.getlist('field[]')
        print(f'{fullname=}')
        #split fullname list into many lists of 5
        split_fullname = [fullname[i:i + 9] for i in range(0, len(fullname), 9)]
        print(f'{split_fullname=}')
        records = []
        for list in split_fullname:
            item = {'sifra': list[0], 
                    'naziv': list[1], 
                    'kolicina': list[2], 
                    'jedinica_mere': list[3], 
                    'cena': list[4], 
                    'popust': list[5],
                    'iznos_popusta': list[6],
                    'iznos_bez_pdv': list[7],
                    'pdv': list[8]}
            records.append(item)
        print(f'{records=}')
        total_price = 0
        try:
            for record in records:
                total_price += (float(record['cena']) * float(record['kolicina']) * (1 - float(record['popust']) / 100))
        except:
            total_price = 0
        print(f'{total_price=}')
        bill.bill_items = records
        if bill.bill_type == 'Knjižno odobrenje':
            bill.total_price = -total_price
        else:
            bill.total_price = total_price
        if company_settings.payment_records:
            payments_list = request.form.getlist('payment[]')
            print(f'{payments_list=}')
            split_payments_list = [payments_list[i:i + 2] for i in range(0, len(payments_list), 2)]
            print(f'{split_payments_list=}')
            records = []
            for list in split_payments_list:
                item = {'payment_date': list[0], 'payment_amount': list[1]}
                records.append(item)
            print(f'{records=}')
            total_payments = 0
            try:
                for record in records:
                    total_payments += int(record['payment_amount'])
            except:
                total_payments = 0
            print(f'{total_payments=}')
            bill.bill_payments = records
            if bill.bill_type == 'Knjižno odobrenje':
                bill.total_payments = -total_payments
            else:
                bill.total_payments = total_payments
            
        if request.form.get('send') == 'Pošaljite dokument':
            bill.bill_status = 'poslat'
            bill.bill_creation_date = date.today()
        elif request.form.get('send') == 'Stornirajte dokument':
            bill.bill_status = 'storniran'
        db.session.commit()
        bill.bill_pdf = pdf_gen(bill)
        db.session.commit()
        flash(f'Dokument {bill.bill_number} je uspesno izmenjen.', 'success')
        return redirect(url_for('bills.bill_list'))
    elif request.method == 'GET':
        form.bill_currency.data = bill.bill_currency
        form.bill_number.data = bill.bill_number
        form.bill_tax_category.data = bill.bill_tax_category
        form.bill_base_code.data = bill.bill_base_code
        form.bill_decision_number.data = bill.bill_decision_number
        form.bill_contract_number.data = bill.bill_contract_number
        form.bill_service.data = bill.bill_service
        form.bill_purchase_order_number.data = bill.bill_purchase_order_number
        if bill.bill_type in ['Faktura']:
            form.bill_transaction_date.data = bill.bill_transaction_date.strftime('%Y-%m-%d')
        if not bill.bill_type in ['Knjižno odobrenje']:
            form.bill_tax_calculation_date.data = bill.bill_tax_calculation_date
            form.bill_due_date.data = bill.bill_due_date.strftime('%Y-%m-%d')
        
        form.bill_reference_number.data = bill.bill_reference_number
        form.bill_model.data = bill.bill_model
        form.bill_attachment.data = bill.bill_attachment
        form.bill_customer_id.data = str(bill.bill_customer_id)
        
    return render_template('bill.html', company_settings = company_settings,
                            form=form, 
                            bill=bill, 
                            units=units, 
                            taxes=taxes,
                            title=title, 
                            dinar_accounts=dinar_accounts,
                            foreign_accounts=foreign_accounts,
                            legend = 'Detalji fakture')


@bills.route("/new_item", methods=['GET', 'POST'])
def new_item():
    new_item_form = f'''
    <tr >
        <td><input class="form-control" type="text" name="field[]"></td>
        <td><input class="form-control" type="text" name="field[]"></td>
        <td><input class="form-control" type="number" name="field[]" value="0" oninput="updateCalculation(this)"></td>
        <td>
            <select class="form-select" name="field[]" id="">
                <option value="kWh">kWh</option>
                <option value="kom">kom</option>
                <option value="kg">kg</option>
                <option value="km">km</option>
                <option value="g">g</option>
                <option value="m">metar</option>
                <option value="l">litar</option>
                <option value="t">tona</option>
                <option value="m2">m2</option>
                <option value="m3">m3</option>
                <option value="min">min</option>
                <option value="h">sat</option>
                <option value="d">dan</option>
                <option value="M">dan</option>
                <option value="god">godina</option>
            </select>
        </td>
        <td><input class="form-control" type="number" name="field[]" value="0" oninput="updateCalculation(this)"></td>
        <td><input class="form-control" type="number" name="field[]" value="0" oninput="updateCalculation(this)"></td>
        <td><input class="form-control" type="text" name="field[]" value="proračun" readonly></td>
        <td><input class="form-control" type="text" name="field[]" value="proračun" readonly></td>
        <td>
            <select class="form-select" name="field[]" id="">
                <option value="0">0%</option>
                <option value="10">10%</option>
                <option value="20">20%</option>
            </select>
        </td>
        <td><button type="button" hx-delete="/delete_item" class="btn btn-danger"><i class="fa-solid fa-minus"></i></button></td>
    </tr>
    '''    
    return new_item_form


@bills.route("/new_payment", methods=['GET', 'POST'])
def new_payment():
    new_payment_form = '''
    <tr>
        <td><input type="date" name="payment[]" class="form-control"></td>
        <td><input type="text" name="payment[]" class="form-control"></td>
        <td><button type="button" hx-delete="/delete_item" class="btn btn-danger"><i class="fa-solid fa-minus"></i></button></td>
    </tr>
    '''
    return new_payment_form


@bills.route("/delete_item", methods=['DELETE'])
def delete_item():
    form = ''
    return form


@bills.route('/open_pdf/<int:bill_id>')
def open_pdf(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    print(f'{bill.bill_pdf=}')
    filename = f'static/bills_data/{bill.bill_pdf}'
    return send_file(filename, mimetype='application/pdf')
