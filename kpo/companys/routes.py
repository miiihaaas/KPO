import secrets, os
from PIL import Image
from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from kpo import db, app
from kpo.companys.forms import RegistrationCompanyForm, EditCompanyForm
from kpo.models import Company
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
                            company_logo='',
                            dinar_account_list=form.dinar_account_list.data,
                            foreign_account_list=form.foreign_account_list.data
                            )
        db.session.add(company)
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
    while len(form.foreign_account_list) < len(company.foreign_account_list):
        form.foreign_account_list.append_entry()
    if request.method == 'POST' and 'add_account' in request.form:
        print('Kliknuto je dugme sa ID-om "add_account"!')
        form.foreign_account_list.append_entry()
    elif request.method == 'POST':
        for key in request.form.keys():
            if key.startswith('remove_account_'):
                remove_account_name = key
                print(f'Kliknuto je dugme sa nazivom {remove_account_name}!')
                remove_account_index = int(remove_account_name.split('_')[-1])
                print(f'Kliknuto je dugme sa indeksom {remove_account_index}!')
                form.foreign_account_list.entries.pop(remove_account_index)
                company.foreign_account_list = form.foreign_account_list.data
                db.session.commit()
                return redirect(url_for('companys.company_profile', company_id=company.id) + '#DevizniRacuni') #! u html fajlu <legend id="DevizniRacuni">

    
    if form.validate_on_submit():
        print('forma je validna')
        if form.company_logo.data:
            picture_file = save_picture(form.company_logo.data)
            company.company_logo=picture_file
        # Update the fields in dinar_account_list and foreign_account_list        
        company.dinar_account_list=form.dinar_account_list.data
        foreign_account_list = []
        for field in form.foreign_account_list:
            account = field.account.data
            iban = field.iban.data
            swift = field.swift.data
            csrf_token = field.csrf_token.data
            foreign_account_list.append({'account': account, 'iban': iban, 'swift': swift, 'csrf_token': csrf_token})
        print(f'nakon validacije: {foreign_account_list=}')
        company.foreign_account_list = foreign_account_list

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
        form.company_logo.data=company.company_logo
        # Set the data for dinar_account_list
        for i, field in enumerate(form.dinar_account_list):
            if i < len(company.dinar_account_list):
                field.data = company.dinar_account_list[i]
        # Set the data for foreign_account_list
        for i, subform in enumerate(form.foreign_account_list):
            if i < len(company.foreign_account_list):
                subform.account.data = company.foreign_account_list[i]['account']
                subform.iban.data = company.foreign_account_list[i]['iban']
                subform.swift.data = company.foreign_account_list[i]['swift']
    elif request.method == 'POST':
        if not form.validate():
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field '{getattr(form, field).label.text}' raised error: {error}")


    image_file = url_for('static', filename='company_logos/' + company.company_logo)
    print(image_file)
    return render_template('company.html', title='Uređivanje podataka kompanije', company=company, form=form, legend='Uređivanje podataka kompanije', image_file=image_file)


@companys.route("/api/testing", methods=['GET'])
def test():    
    # form = RegistrationCompanyForm()
    form = '''<!DOCTYPE html><html>
    <head>
    <title>Test</title>
    </head>
    <body>
    <h1>Test</h1>
    <div>
    <input class="form-control" type="text" name="test" value="test">
    <button class="btn btn-primary" type="submit">Submit</button>
    </div>
    </body>
    </html>'''
    return form