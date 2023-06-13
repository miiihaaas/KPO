import os
import requests
from PIL import Image
import io
from werkzeug.utils import secure_filename
from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Blueprint, Response
from flask import  render_template, redirect, url_for, flash, send_file, request
from sqlalchemy import func
from kpo import db
from kpo.models import Company, Settings, User
from kpo.invoices.forms import DashboardData
from kpo.bills.forms import Dashboard
from kpo.bills.functions import import_data_from_pdv, uplatnice_gen
from kpo.main.forms import SettingsForm, SelectCompanyForm
from flask_login import current_user
from flask import jsonify

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


@main.route("/import_from_pdv", methods=['GET', 'POST'])
def import_from_pdv():    
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('kpo/static/pdf_import/', filename))
        file_path = os.path.join('kpo/static/pdf_import/', filename)
        df = import_data_from_pdv(file_path)
        df_list = df.values.tolist()
        qr_code_images = []
        for i, record in enumerate(df_list):
            racun = record[1]
            racun = racun.replace('-', '')  # Uklanja sve crtice iz računa
            racun = racun[:3] + racun[3:].zfill(15)  # Dodaje nule posle prvih 3 cifre računa do ukupne dužine od 18 cifara
            dug = record[2]
            dug = "RSD" + str(dug).replace('.', ',')
            data = {
                "K": "PR",
                "V": "01",
                "C": "1",
                "R": racun,
                "N": "PORESKA UPRAVA\r\nSAVE MAŠKOVIĆA 3-5",
                "I": dug,
                "P": "UPLATILAC PREZIME\r\nŽUPSKA 13\r\nBEOGRAD 6",
                "SF": "189", #! šifra plaćanja - Marko
                "S": record[3],
                "RO": record[4]+record[5]
            }
            print(f'{data=}')
            #! dokumentacija: https://ips.nbs.rs/PDF/Smernice_Generator_Validator_latinica_feb2023.pdf
            url = 'https://nbs.rs/QRcode/api/qr/v1/gen/250'
            headers = { 'Content-Type': 'application/json' }
            response = requests.post(url, headers=headers, json=data)
            print(f'{response=}')
            if response.status_code == 500:
                print(response.content)
                print(response.headers)
                response_data = response.json()
                if 'error_message' in response_data:
                    error_message = response_data['error_message']
                    print(f"Error message: {error_message}")

            if response.status_code == 200:
                qr_code_image = Image.open(io.BytesIO(response.content))
                qr_code_filename = f'qr_{i}.png'
                qr_code_image.save(os.path.join('kpo/static/payment_slips/qr_code/', qr_code_filename))
                qr_code_filepath = os.path.join('kpo/static/payment_slips/qr_code/', qr_code_filename)
                with open(qr_code_filepath, 'wb') as file:
                    file.write(response.content)
                qr_code_images.append(qr_code_filename)
            else:
                pass
                # return 'Error generating QR code', response.status_code
        print(f'{qr_code_images=}')
            # if response.status_code == 200:
            #     qr_code_image = response.content
            #     qr_code_image = response.content
            #     return Response(qr_code_image, mimetype="image/png")
            # else:
            #     return 'Error generating QR code', response.status_code
        gen_file = uplatnice_gen(df_list, qr_code_images)
        
        #! briše QR kodove nakon dodavanja na uplatnice
        folder_path = 'kpo/static/payment_slips/qr_code/'
        # Provjeri da li je putanja zaista direktorijum
        if os.path.isdir(folder_path):
            # Prolazi kroz sve fajlove u direktorijumu
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                # Provjeri da li je trenutni element fajl
                if os.path.isfile(file_path):
                    # Obriši fajl
                    os.remove(file_path)
            print("Svi fajlovi su uspješno obrisani.")
        else:
            print("Navedena putanja nije direktorijum.")

        
        filename = f'static/payment_slips/uplatnice.pdf'
        return render_template('import_from_pdv.html', title='Import iz PDVa', df=df.values.tolist()) #! ova dva spojiti
        return send_file(filename, mimetype='application/pdf', as_attachment=True) #! ova dva spojiti
    return render_template('import_from_pdv.html', title='Import iz PDVa')


@main.route("/generate_uplatnice", methods=['GET', 'POST'])
def generate_uplatnice():
    df_list = [['711122', '840-711122843-32', 30130.02, 'POREZ - PAUŠAL', '97', '92011108882322'], 
                ['711122', '840-711122843-32', 51033.11, 'POREZ - PAUŠAL', '97', '1701190000002887096'], 
                ['711122', '840-711122843-32', 65498.1, 'POREZ - PAUŠAL', '97', '2701190000003677093'], 
                ['711122', '840-711122843-32', 55.17, 'POREZ - PAUŠAL', '97', '5801190000002477613'], 
                ['711122', '840-711122843-32', 8.53, 'POREZ - PAUŠAL', '97', '6101190000004566507'], 
                ['711122', '840-711122843-32', 12.27, 'POREZ - PAUŠAL', '97', '8901190000001735294'], 
                ['721313', '840-721313843-83', 154.61, 'PIO - PAUŠAL', '97', '1701190000002887096'], 
                ['721313', '840-721313843-83', 130461.36, 'PIO - PAUŠAL', '97', '2701190000003677093'], 
                ['721313', '840-721313843-83', 20.48, 'PIO - PAUŠAL', '97', '6101190000004566507'], 
                ['721313', '840-721313843-83', 32.18, 'PIO - PAUŠAL', '97', '8901190000001735294'], 
                ['721325', '840-721325843-61', 59.69, 'ZDRAVSTVENO OSIGURANJE - PAUŠAL', '97', '1701190000002887096'], 
                ['721325', '840-721325843-61', 27169.13, 'ZDRAVSTVENO OSIGURANJE - PAUŠAL', '97', '2701190000003677093'], 
                ['721325', '840-721325843-61', 50791.75, 'ZDRAVSTVENO OSIGURANJE - PAUŠAL', '97', '5801190000002477613'], 
                ['721325', '840-721325843-61', 8.79, 'ZDRAVSTVENO OSIGURANJE - PAUŠAL', '97', '6101190000004566507'], 
                ['721325', '840-721325843-61', 11.33, 'ZDRAVSTVENO OSIGURANJE - PAUŠAL', '97', '8901190000001735294']]
    gen_file = uplatnice_gen(df_list)
    filename = f'static/bills_data/uplatnice.pdf'
    return send_file(filename, mimetype='application/pdf')