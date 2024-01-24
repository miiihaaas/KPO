import secrets, os
from PIL import Image
from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from kpo import db, app
from kpo.companys.forms import RegistrationCompanyForm, EditCompanyForm
from kpo.models import Company, Settings
from flask import jsonify

companys = Blueprint('companys', __name__)


@companys.route("/company_list")
def company_list():
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    companys = Company.query.all()
    return render_template('company_list.html', title='Kompanija', companys=companys)


@companys.route("/register_c", methods=['GET', 'POST'])
def register_c():
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.is_authenticated and current_user.authorization != 's_admin':
        return redirect(url_for('main.home'))
    form = RegistrationCompanyForm()
    if form.validate_on_submit():
        dinar_account_list = request.form.getlist('dinar_account[]')
        foreign_account_list = request.form.getlist('foreign_account[]')
        print(f'{foreign_account_list=}')
        split_foreign_account_list = [foreign_account_list[i:i + 3] for i in range(0, len(foreign_account_list), 3)]
        print(f'{split_foreign_account_list=}')
        records = []
        for list in split_foreign_account_list:
            item = {
                'account': list[0],
                'iban': list[1],
                'swift': list[2]
            }
            records.append(item)
        print(f'{records=}')
        company = Company(companyname=form.companyname.data,
                            company_address=form.company_address.data,
                            company_address_number=form.company_address_number.data,
                            company_zip_code=form.company_zip_code.data,
                            company_city=form.company_city.data,
                            company_state=form.company_state.data,
                            company_pib=form.company_pib.data,
                            company_mb=form.company_mb.data,
                            company_jbkjs=form.company_jbkjs.data,
                            company_site=form.company_site.data,
                            company_mail=form.company_mail.data,
                            company_phone=form.company_phone.data,
                            company_default_tax_category = form.company_default_tax_category.data,
                            company_default_base_code = form.company_default_base_code.data,
                            company_logo='',
                            dinar_account_list=dinar_account_list,
                            foreign_account_list=records
                            )
        db.session.add(company)
        db.session.commit()
        settings = Settings(company_id=company.id,
                            synchronization_with_eFaktura=0,
                            payment_records=0,
                            synchronization_with_CRF=0,
                            forward_invoice_to_customer=0)
        db.session.add(settings)
        db.session.commit()
        flash(f'Kompanija: {form.companyname.data} je uspešno kreirana.', 'success')
        return redirect(url_for('main.home'))
    return render_template('register_c.html', title='Registracija nove kompanije', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/company_logos', picture_fn)
    form_picture.save(picture_path)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@companys.route("/company/<int:company_id>", methods=['GET', 'POST'])
# @login_required
def company_profile(company_id): #ovo je funkcija za editovanje user-a
    company = Company.query.get_or_404(company_id)
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization != 's_admin' and current_user.authorization != 'c_admin':
        abort(403)
    elif current_user.user_company.id != company.id and current_user.authorization != 's_admin':
        abort(403)
    form = EditCompanyForm()
    
    if form.validate_on_submit():
        if form.company_logo.data:
            picture_file = save_picture(form.company_logo.data)
            company.company_logo=picture_file
        # Update the fields in dinar_account_list and foreign_account_list        
        foreign_account_list = request.form.getlist('foreign_account[]')
        print(f'{foreign_account_list=}')
        split_foreign_account_list = [foreign_account_list[i:i + 3] for i in range(0, len(foreign_account_list), 3)]
        print(f'{split_foreign_account_list=}')
        records = []
        for list in split_foreign_account_list:
            item = {
                'account': list[0],
                'iban': list[1],
                'swift': list[2]
            }
            records.append(item)
        print(f'{records=}')
        company.foreign_account_list = records
        
        dinar_account_list = request.form.getlist('dinar_account[]')
        print(f'{dinar_account_list=}')
        company.dinar_account_list = dinar_account_list

        company.companyname=form.companyname.data
        company.company_address=form.company_address.data
        company.company_address_number=form.company_address_number.data
        company.company_zip_code=form.company_zip_code.data
        company.company_city=form.company_city.data
        company.company_state=form.company_state.data
        company.company_pib=form.company_pib.data
        company.company_mb=form.company_mb.data
        company.company_jbkjs=form.company_jbkjs.data
        company.company_site=form.company_site.data
        company.company_mail=form.company_mail.data
        company.company_phone=form.company_phone.data
        company.company_default_tax_category = form.company_default_tax_category.data
        company.company_default_base_code = form.company_default_base_code.data
        db.session.commit()
        flash(f'Podaci kompanije {company.companyname} su izmenjeni.', 'success')
        return redirect(url_for('companys.company_list', title='Kompanija', companys=companys))
    elif request.method == 'GET':
        form.companyname.data=company.companyname
        form.company_address.data=company.company_address
        form.company_address_number.data=company.company_address_number
        form.company_zip_code.data=company.company_zip_code
        form.company_city.data=company.company_city
        form.company_state.data=company.company_state
        form.company_pib.data=company.company_pib
        form.company_mb.data=company.company_mb
        form.company_jbkjs.data=company.company_jbkjs
        form.company_site.data=company.company_site
        form.company_mail.data=company.company_mail
        form.company_phone.data=company.company_phone
        form.company_default_tax_category.data=company.company_default_tax_category
        form.company_default_base_code.data=company.company_default_base_code
        form.company_logo.data=company.company_logo

    elif request.method == 'POST':
        if not form.validate():
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field '{getattr(form, field).label.text}' raised error: {error}")


    image_file = url_for('static', filename='company_logos/' + company.company_logo)
    print(image_file)
    return render_template('company.html', title='Uređivanje podataka kompanije', company=company, form=form, legend='Uređivanje podataka kompanije', image_file=image_file)


@companys.route("/new_foreign_account", methods=['GET', 'POST'])
def new_foreign_account():
    new_item_form = f'''
    <tr >
        <td><input class="form-control" type="text" name="foreign_account[]"></td>
        <td><input class="form-control" type="text" name="foreign_account[]"></td>
        <td><input class="form-control" type="text" name="foreign_account[]"></td>
        <td><button type="button" hx-delete="/delete_account" class="btn btn-danger">-</button></td>
    </tr>
    '''
    return new_item_form


@companys.route("/new_dinar_account", methods=['GET', 'POST'])
def new_dinar_account():
    new_item_form = f'''
    <tr >
        <td><input class="form-control" type="text" name="dinar_account[]"></td>
        <td><button type="button" hx-delete="/delete_account" class="btn btn-danger">-</button></td>
    </tr>
    '''
    return new_item_form


@companys.route("/delete_account", methods=['DELETE'])
def delete_foreign_account():
    form = ''
    return form