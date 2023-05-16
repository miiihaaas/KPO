from datetime import datetime
from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from kpo import db, app
from kpo.models import Bill, Customer, Settings
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
            bill_customer_id = form.bill_customer_id.data,
            bill_items = [{'sifra': '', 'naziv': '', 'kolicina': '', 'jedinica_mere': '', 'cena': ''}]
        )
        db.session.add(bill)
        db.session.commit()
        return redirect(url_for('bills.bill_profile', bill_id=bill.id) + '#stavke')
    return render_template('register_b.html', title='Registracija nove fakture', form=form)
    
    
@bills.route("/bill/<int:bill_id>", methods=['GET', 'POST'])
def bill_profile(bill_id):
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    bill = Bill.query.get_or_404(bill_id)
    company_settings = Settings.query.filter_by(id=current_user.company_id).first()
    form = EditBillForm()
    form.bill_customer_id.choices = [(c.id, c.customer_name) for c in Customer.query.filter_by(company_id=current_user.company_id).all()]
    units = [('kWh', 'kWh'), ('kom', 'kom'), ('kg', 'kg'), ('km', 'km'), ('g', 'g'), ('m', 'metar'), ('l', 'litar'), ('t', 'tona'), ('m2', 'm2'), ('m3', 'm3'), ('min', 'min'), ('h', 'sat'), ('d', 'dan'), ('M', 'mesec'), ('god', 'godina')]
    taxes = [('0', '0%'), ('10', '10%'), ('20', '20%')]
    if form.validate_on_submit():
        bill.bill_currency = form.bill_currency.data
        bill.bill_type = form.bill_type.data
        bill.bill_number = form.bill_number.data
        bill.bill_tax_category = form.bill_tax_category.data
        bill.bill_base_code = form.bill_base_code.data
        bill.bill_decision_number = form.bill_decision_number.data
        bill.bill_contract_number = form.bill_contract_number.data
        bill.bill_service = form.bill_service.data
        bill.bill_purchase_order_number = form.bill_purchase_order_number.data
        bill.bill_transaction_date = datetime.strptime(form.bill_transaction_date.data, '%Y-%m-%d')
        bill.bill_due_date = datetime.strptime(form.bill_due_date.data, '%Y-%m-%d')
        bill.bill_tax_calculation_date = form.bill_tax_calculation_date.data
        bill.bill_reference_number = form.bill_reference_number.data
        bill.bill_model = form.bill_model.data
        bill.bill_attachment = form.bill_attachment.data
        bill.bill_customer_id = form.bill_customer_id.data
        
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
        for record in records:
            total_price += (int(record['cena']) * int(record['kolicina']))
        print(f'{total_price=}')
        bill.bill_items = records
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
            for record in records:
                total_payments += int(record['payment_amount'])
            print(f'{total_payments=}')
            bill.bill_payments = records
            bill.total_payments = total_payments
        
        db.session.commit()
        flash(f'Dokument {bill.bill_number} je uspesno izmenjen.', 'success')
        return redirect(url_for('bills.bill_list'))
    elif request.method == 'GET':
        form.bill_currency.data = bill.bill_currency
        form.bill_type.data = bill.bill_type
        form.bill_number.data = bill.bill_number
        form.bill_tax_category.data = bill.bill_tax_category
        form.bill_base_code.data = bill.bill_base_code
        form.bill_decision_number.data = bill.bill_decision_number
        form.bill_contract_number.data = bill.bill_contract_number
        form.bill_service.data = bill.bill_service
        form.bill_purchase_order_number.data = bill.bill_purchase_order_number
        form.bill_transaction_date.data = bill.bill_transaction_date.strftime('%Y-%m-%d')
        form.bill_due_date.data = bill.bill_due_date.strftime('%Y-%m-%d')
        form.bill_tax_calculation_date.data = bill.bill_tax_calculation_date
        form.bill_reference_number.data = bill.bill_reference_number
        form.bill_model.data = bill.bill_model
        form.bill_attachment.data = bill.bill_attachment
        form.bill_customer_id.data = str(bill.bill_customer_id)
        
    return render_template('bill.html', company_settings = company_settings,
                            form=form, 
                            bill=bill, 
                            units=units, 
                            taxes=taxes,
                            title='Detalji fakture', 
                            legend = 'Detalji fakture')


@bills.route("/new_item", methods=['GET', 'POST'])
def new_item():
    new_item_form = f'''
    <tr >
        <td><input class="form-control" type="text" name="field[]"></td>
        <td><input class="form-control" type="text" name="field[]"></td>
        <td><input class="form-control" type="text" name="field[]"></td>
        <td><input class="form-control" type="text" name="field[]"></td>
        <td><input class="form-control" type="text" name="field[]"></td>
        <td><input class="form-control" type="text" name="field[]" ></td>
        <td><input class="form-control" type="text" name="field[]" value="proračun" readonly></td>
        <td><input class="form-control" type="text" name="field[]" value="proračun" readonly></td>
        <td>
            <select class="form-select" name="field[]" id="">
                <option value="0">0%</option>
                <option value="10">10%</option>
                <option value="20">20%</option>
            </select>
        </td>
        <td><button type="button" hx-delete="/delete_item" class="btn btn-danger">-</button></td>
    </tr>
    '''
    return new_item_form


@bills.route("/new_payment", methods=['GET', 'POST'])
def new_payment():
    new_payment_form = '''
    <tr>
        <td><input type="date" name="payment[]" class="form-control"></td>
        <td><input type="text" name="payment[]" class="form-control"></td>
        <td><button type="button" hx-delete="/delete_item" class="btn btn-danger">-</button></td>
    </tr>
    '''
    return new_payment_form


@bills.route("/delete_item", methods=['DELETE'])
def delete_item():
    form = ''
    return form