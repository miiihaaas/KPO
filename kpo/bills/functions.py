from fpdf import FPDF
import pdfplumber
import pandas as pd
from datetime import datetime


def import_data_from_pdv(file):
    dependent_dict = [
    {
        "Konto": '711122',
        "Broj računa": "840-711122843-32",
        "Ukupan dug": "Pročitati iz PDF dokumenta",
        "Opis-svrha uplate": "POREZ - PAUŠAL",
        "Model": '97',
        "Poziv na broj": "Pročitati iz PDF dokumenta"
    },
    {
        "Konto": '721313',
        "Broj računa": "840-721313843-74", #!Marko: da nije 840-721313843-74? vs 840-721313843-83
        "Ukupan dug": "Pročitati iz PDF dokumenta",
        "Opis-svrha uplate": "PIO - PAUŠAL",
        "Model": '97',
        "Poziv na broj": "Pročitati iz PDF dokumenta"
    },
    {
        "Konto": '721325',
        "Broj računa": "840-721325843-61",
        "Ukupan dug": "Pročitati iz PDF dokumenta",
        "Opis-svrha uplate": "ZDRAVSTVENO OSIGURANJE - PAUŠAL",
        "Model": '97',
        "Poziv na broj": "Pročitati iz PDF dokumenta"
    },
    {
        "Konto": '721221',
        "Broj računa": "840-721331843-06",
        "Ukupan dug": "Pročitati iz PDF dokumenta",
        "Opis-svrha uplate": "NEZAPOSLENOST - PAUŠAL",
        "Model": '97',
        "Poziv na broj": "Pročitati iz PDF dokumenta"
    },
    {
        "Konto": '721419',
        "Broj računa": "840-721419843-40",
        "Ukupan dug": "Pročitati iz PDF dokumenta",
        "Opis-svrha uplate": "PIO - PAUŠAL - IZ RADNOG ODNOSA",
        "Model": '97',
        "Poziv na broj": "Pročitati iz PDF dokumenta"
    },
    # {
    #     "Konto": '721331',
    #     "Broj računa": "Simke duguje podatke", #! 840-721331843-06?
    #     "Ukupan dug": "Pročitati iz PDF dokumenta",
    #     "Opis-svrha uplate": "Simke duguje podatke",
    #     "Model": '97',
    #     "Poziv na broj": "Pročitati iz PDF dokumenta"
    # }
]

    db = []
    with pdfplumber.open(file) as f:
        for page in f.pages:
            # Postavite horizontal_text_tolerance na veću vrednost (npr. 10)
            page.horizontal_text_tolerance = 100
            tables = page.extract_tables()
            counter = 0
            for table in tables:
                if counter == 0:
                    uplatilac = pd.DataFrame(table[0:], columns=table[0])
                    print(f'ovo bi trebalo da je tabela sa podacima uplatioca: {uplatilac=}')
                    print(f'{len(uplatilac)}')
                    print(f'{uplatilac.iloc[1, 0]=}')
                if counter % 2 == 1:  # Dodaj samo tabele sa neparanim brojem
                    df = pd.DataFrame(table[1:], columns=table[0])
                    db.append(df)
                counter += 1
    # print(f'{db=}')
    # print(f'{len(db)=}')
    # Spajanje svih DataFrame-ova u db
    combined_df = pd.concat(db)
    
    # Resetovanje indeksa u rastućem redosledu
    combined_df = combined_df.reset_index(drop=True)
    # print(f'{combined_df=}')
    # print(f'{len(combined_df)=}')
    
    # Konvertovanje kolone 'Ukupandug' u numerički tip podataka
    combined_df['Ukupandug'] = combined_df['Ukupandug'].str.replace(',', '').astype(float)
    # print(f'{combined_df["Ukupandug"]=}')
    
    # Filtriranje redova na osnovu vrednosti u koloni 'Ukupandug'
    combined_df = combined_df.loc[combined_df['Ukupandug'] > 0]
    
    # Kreiranje DataFrame-a 'uplatnice_df' na osnovu filtriranih vrednosti
    uplatnice_df = pd.DataFrame(columns=["Konto", "Broj računa", "Ukupan dug", "Opis-svrha uplate", "Model", "Poziv na broj"])
    
    for _, row in combined_df.iterrows():
        konto = row['Konto']
        matching_dict = next((item for item in dependent_dict if item['Konto'] == konto), None)
        if matching_dict:
            new_row = pd.DataFrame([[
                matching_dict['Konto'],
                matching_dict['Broj računa'],
                row['Ukupandug'],
                matching_dict['Opis-svrha uplate'],
                matching_dict['Model'],
                row['Pozivnabroj']
            ]], columns=["Konto", "Broj računa", "Ukupan dug", "Opis-svrha uplate", "Model", "Poziv na broj"])
            uplatnice_df = pd.concat([uplatnice_df, new_row], ignore_index=True)

    return uplatnice_df


def uplatnice_gen(df_list, qr_code_images):
    class PDF(FPDF):
        def __init__(self, **kwargs):
            super(PDF, self).__init__(**kwargs)
            self.add_font('DejaVuSansCondensed', '', './kpo/static/fonts/DejaVuSansCondensed.ttf', uni=True)
            self.add_font('DejaVuSansCondensed', 'B', './kpo/static/fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
    pdf = PDF()
    # pdf.add_page()
    counter = 1
    for i, uplatnica in enumerate(df_list):
        print(uplatnica)
        if counter % 3 == 1:
            pdf.add_page()
            y = 0
            y_qr = 50
            pdf.line(210/2, 10, 210/2, 237/3)
        elif counter % 3 == 2:
            y = 99
            y_qr = 149
            pdf.line(210/2, 110, 210/2, 99+237/3)
        elif counter % 3 == 0:
            y = 198
            y_qr = 248
            pdf.line(210/2, 210, 210/2, 198+237/3)
        pdf.set_font('DejaVuSansCondensed', 'B', 16)
        pdf.set_y(y_qr)
        pdf.set_x(175)
        pdf.image(f'kpo/static/payment_slips/qr_code/{qr_code_images[i]}' , w=25)
        pdf.set_y(y+8)
        pdf.cell(0,8, f"NALOG ZA UPLATU", new_y='NEXT', new_x='LMARGIN', align='R', border=0)
        pdf.set_font('DejaVuSansCondensed', '', 10)
        pdf.cell(95,4, f"Uplatilac", new_y='NEXT', new_x='LMARGIN', align='L', border=0)
        pdf.multi_cell(90,4, f'''Marko Marković\r\n{''}\r\n{''}''', new_y='NEXT', new_x='LMARGIN', align='L', border=1)
        pdf.cell(95,4, f"Svrha uplate", new_y='NEXT', new_x='LMARGIN', align='L', border=0)
        pdf.multi_cell(90,4, f'''{uplatnica[3]}\r\n{''}\r\n{''}''', new_y='NEXT', new_x='LMARGIN', align='L', border=1)
        pdf.cell(95,4, f"Primalac", new_y='NEXT', new_x='LMARGIN', align='L', border=0)
        pdf.multi_cell(90,4, f'''PORESKA UPRAVA\r\n{''}\r\n{''}''', new_y='NEXT', new_x='LMARGIN', align='L', border=1)
        pdf.cell(95,1, f"", new_y='NEXT', new_x='LMARGIN', align='L', border=0)
        pdf.set_font('DejaVuSansCondensed', '', 7)
        pdf.cell(50,4, f"Pečat i potpis uplatioca", new_y='NEXT', new_x='LMARGIN', align='L', border='T')
        pdf.cell(95,1, f"", new_y='NEXT', new_x='LMARGIN', align='L', border=0)
        pdf.set_x(50)
        pdf.cell(50,4, f"Mesto i datum prijema", new_y='LAST', align='L', border='T')
        pdf.set_x(110)
        pdf.cell(40,5, f"Datum valute", align='L', border='T')
        pdf.set_y(y + 15)
        pdf.set_x(110)
        pdf.set_font('DejaVuSansCondensed', '', 8)
        pdf.multi_cell(13,3, f"Šifra plaćanja", new_y='LAST', align='L', border=0)
        pdf.multi_cell(7,3, f"", new_y='LAST', align='L', border=0)
        pdf.multi_cell(13,3, f"Valuta", new_y='LAST', align='L', border=0)
        pdf.multi_cell(10,3, f"", new_y='LAST', align='L', border=0)
        pdf.multi_cell(13,3, f"Iznos", new_y='NEXT', align='L', border=0)
        pdf.set_x(110)
        pdf.set_font('DejaVuSansCondensed', '', 10)
        pdf.multi_cell(13,6, f"189", new_y='LAST', align='L', border=1)
        pdf.multi_cell(7,6, f"", new_y='LAST', align='L', border=0)
        pdf.multi_cell(13,6, f"RSD", new_y='LAST', align='L', border=1)
        pdf.multi_cell(10,6, f"", new_y='LAST', align='L', border=0)
        pdf.multi_cell(47,6, f"{uplatnica[2]}", new_y='NEXT', align='L', border=1)
        pdf.set_x(110)
        pdf.set_font('DejaVuSansCondensed', '', 8)
        pdf.multi_cell(90,5, f"Račun primaoca", new_y='NEXT', align='L', border=0)
        pdf.set_x(110)
        pdf.set_font('DejaVuSansCondensed', '', 10)
        pdf.multi_cell(90,6, f"{uplatnica[1]}", new_y='NEXT', align='L', border=1)
        pdf.set_x(110)
        pdf.set_font('DejaVuSansCondensed', '', 8)
        pdf.multi_cell(90,5, f"Model i poziv na broj (odobrenje)", new_y='NEXT', align='L', border=0)
        pdf.set_x(110)
        pdf.set_font('DejaVuSansCondensed', '', 10)
        pdf.multi_cell(10,6, f"{uplatnica[4]}", new_y='LAST', align='L', border=1)
        pdf.multi_cell(10,6, f"", new_y='LAST', align='L', border=0)
        pdf.multi_cell(70,6, f"{uplatnica[5]}", new_y='LAST', align='L', border=1)
        
        pdf.line(10, 99, 200, 99)
        pdf.line(10, 198, 200, 198)
        counter += 1
    path = "kpo/static/payment_slips/"
    file_name = f'uplatnice.pdf'
    pdf.output(path + file_name)
    return file_name
    
    

def pdf_gen(bill):
    company_logo = 'kpo/static/company_logos/' + bill.bill_company.company_logo
    company_name = bill.bill_company.companyname
    company_address = bill.bill_company.company_address
    company_address_number = bill.bill_company.company_address_number
    company_zip_code = bill.bill_company.company_zip_code
    company_city = bill.bill_company.company_city
    company_state = bill.bill_company.company_state
    company_pib = bill.bill_company.company_pib
    company_mb = bill.bill_company.company_mb
    company_phone = bill.bill_company.company_phone
    company_mail = bill.bill_company.company_mail
    company_site = bill.bill_company.company_site
    company_selected_account = bill.bill_company_account
    company_dinar_account_list = bill.bill_company.dinar_account_list
    company_foreign_account_list = bill.bill_company.foreign_account_list
    
    print(f'start debug: {company_selected_account=}')
    if company_selected_account in company_dinar_account_list:
        print('DINAR')
        company_selected_iban = None
        company_selected_swift = None
    else:
        for account_info in company_foreign_account_list:
            if account_info['account'] == company_selected_account:
                company_selected_iban = account_info['iban']
                company_selected_swift = account_info['swift']
                print(f'{company_selected_iban=}')
                print(f'{company_selected_swift=}')
            else:
                company_selected_iban = None
                company_selected_swift = None
    
    
    print(f'{company_dinar_account_list=}')
    print(f'{company_foreign_account_list=}')
    if bill.bill_type == 'Faktura':
        broj_dokumenta = 'Broj fakture'
    elif bill.bill_type == 'Avansni račun':
        broj_dokumenta = 'Broj avansnog računa'
    elif bill.bill_type == 'Knjižno odobrenje':
        broj_dokumenta = 'Broj knjižnog odobrenja'
    elif bill.bill_type == 'Knjižno zaduženje':
        broj_dokumenta = 'Broj knjižnog zaduženja'
    class PDF(FPDF):
        def __init__(self, **kwargs):
            super(PDF, self).__init__(**kwargs)
            self.add_font('DejaVuSansCondensed', '', './kpo/static/fonts/DejaVuSansCondensed.ttf', uni=True)
            self.add_font('DejaVuSansCondensed', 'B', './kpo/static/fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
        def header(self):
            # Logo
            self.image(company_logo, 180, 5, 25)
        def footer(self):
            # Postavljanje fonta
            self.set_font('DejaVuSansCondensed', '', 8)
            
            # Računanje Y pozicije za footer
            page_height = self.h  # Dobavljanje visine stranice
            footer_height = 10  # Visina footera (u mm)
            footer_ypos = page_height - footer_height - 10  # Izračunavanje Y pozicije

            # Postavljanje pozicije za centriranje teksta
            self.set_y(footer_ypos + (footer_height - self.font_size) / 2)

            # Footer tekst
            footer_text = f'{company_name} | {company_city} | {company_mail} | {company_phone} | {company_site}'
            self.cell(0, footer_height, footer_text, ln=False, align='C')
            
    
    pdf=PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('DejaVuSansCondensed', '', 10)
    pdf.set_y(40)  # Prilagodite Y poziciju prema potrebi
    if bill.bill_status == 'storniran':
        print(f'generisanje pdf fajla - status storniran')
        pdf.image('kpo/static/img/storno.jpg', 0, 30, 220)
    if bill.bill_transaction_date:
        pdf.cell(95,6, f"Datum izdavanja: {bill.bill_transaction_date.strftime('%d.%m.%Y.')}", ln=False, align='L')
    else:
        pdf.cell(95,6, f"", ln=False, align='L')
    pdf.set_font('DejaVuSansCondensed', 'B', 10)
    pdf.set_fill_color(192, 192, 192)  # Postavljanje RGB vrijednosti sive boje
    pdf.cell(95,6, f'{broj_dokumenta}', ln=True, align='C', fill=True)
    pdf.set_font('DejaVuSansCondensed', 'B', 15)
    pdf.cell(95,10, f'', ln=False, align='L')
    pdf.cell(95,10, f'{bill.bill_number}', ln=True, align='C')
    pdf.cell(95,10, f'{bill.bill_customer.customer_name}', ln=True, align='L')
    pdf.set_font('DejaVuSansCondensed', '', 12)
    pdf.cell(95,5, f'{bill.bill_customer.customer_address} {bill.bill_customer.customer_address_number}', ln=True, align='L')
    pdf.cell(95,5, f'{bill.bill_customer.customer_zip_code} {bill.bill_customer.customer_city} {bill.bill_customer.customer_state}', ln=True, align='L')
    pdf.set_y(56)  # Prilagodite Y poziciju prema potrebi
    pdf.set_x(105)  # Prilagodite X poziciju prema potrebi
    pdf.set_font('DejaVuSansCondensed', '', 10)
    if bill.bill_transaction_date:
        pdf.cell(48,4, f"Datum prometa", new_y='LAST', align='R')
        pdf.cell(47,4, f"{bill.bill_transaction_date.strftime('%d.%m.%Y.')}", new_y='NEXT', align='L')
    pdf.set_x(105)  # Prilagodite X poziciju prema potrebi
    if bill.bill_due_date:
        pdf.cell(48,4, f"Datum dospeća", new_y='LAST', align='R')
        pdf.set_font('DejaVuSansCondensed', 'B', 10)
        pdf.cell(47,4, f"{bill.bill_due_date.strftime('%d.%m.%Y.')}", new_y='NEXT', align='L')
    pdf.set_x(105)  # Prilagodite X poziciju prema potrebi
    pdf.set_font('DejaVuSansCondensed', '', 10)
    pdf.cell(48,4, f"Matični broj kupca", new_y='LAST', align='R')
    pdf.cell(47,4, f"{bill.bill_customer.customer_mb}", new_y='NEXT', align='L')
    pdf.set_x(105)  # Prilagodite X poziciju prema potrebi
    pdf.cell(48,4, f"PIB kupca", new_y='LAST', align='R')
    pdf.cell(47,4, f"{bill.bill_customer.customer_pib}", new_y='NEXT', align='L')
    pdf.set_font('DejaVuSansCondensed', '', 12)
    pdf.set_x(105)  # Prilagodite X poziciju prema potrebi
    pdf.cell(48,6, f"Valuta", new_y='LAST', align='R')
    pdf.set_font('DejaVuSansCondensed', 'B', 15)
    pdf.cell(47,6, f"{bill.bill_currency}", new_y='NEXT', align='L')
    pdf.set_x(105)  # Prilagodite X poziciju prema potrebi
    pdf.set_font('DejaVuSansCondensed', '', 12)
    if bill.bill_type != 'Knjižno odobrenje':
        pdf.cell(48,6, f"Ukupno za plaćanje", new_y='LAST', align='R')
        pdf.set_font('DejaVuSansCondensed', 'B', 15)
        pdf.cell(47,6, "{:,.2f}".format(bill.total_price).replace(",", " ").replace(".", ",").replace(" ", "."), new_y='NEXT', align='L')
    else:
        pdf.cell(48,6, f"Ukupno odobrenje", new_y='LAST', align='R')
        pdf.set_font('DejaVuSansCondensed', 'B', 15)
        pdf.cell(47,6, "{:,.2f}".format(-bill.total_price).replace(",", " ").replace(".", ",").replace(" ", "."), new_y='NEXT', align='L')
    pdf.set_x(10)  # Prilagodite X poziciju prema potrebi
    pdf.set_font('DejaVuSansCondensed', 'B', 10)
    pdf.cell(0,6, f'', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.cell(0,6, f'Prodavac', new_x='LMARGIN', new_y='NEXT', align='L', border='B')
    pdf.set_font('DejaVuSansCondensed', 'B', 15)
    pdf.cell(0,10, f'{company_name}', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.set_font('DejaVuSansCondensed', '', 10)
    if not bill.bill_type == 'Knjižno odobrenje':
        pdf.cell(120,4, f'{company_address} {company_address_number}, {company_zip_code} {company_city}, {company_state}', new_y='LAST', align='L')
        pdf.cell(20,4, f'broj računa: ', new_y='LAST', align='R')
        pdf.cell(50,4, f'{company_selected_account}', new_x='LMARGIN', new_y='NEXT', align='L')
    else:
        pdf.cell(0,4, f'{company_address} {company_address_number}, {company_zip_code} {company_city}, {company_state}', new_x='LMARGIN', new_y='NEXT', align='L')
    if company_selected_iban:
        pdf.cell(120,4, f'Matični broj: {company_mb}', new_y='LAST', align='L')
        pdf.cell(20,4, f'IBAN: ', new_y='LAST', align='R')
        pdf.cell(50,4, f'{company_selected_iban}', new_x='LMARGIN', new_y='NEXT', align='L')
    else:
        pdf.cell(0,4, f'Matični broj: {company_mb}', new_x='LMARGIN', new_y='NEXT', align='L')
    if company_selected_swift:
        pdf.cell(120,4, f'PIB: {company_pib}', new_y='LAST', align='L')
        pdf.cell(20,4, f'SWIFT: ', new_y='LAST', align='R')
        pdf.cell(50,4, f'{company_selected_swift}', new_x='LMARGIN', new_y='NEXT', align='L')
    else:
        pdf.cell(0,4, f'PIB: {company_pib}', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.cell(0,3, f'', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.cell(55,4, f'Opis', new_y='LAST', align='L', fill=1)
    pdf.cell(20,4, f'Količina', new_y='LAST', align='R', fill=1)
    pdf.cell(25,4, f'Jedinica mere', new_y='LAST', align='R', fill=1)
    pdf.cell(25,4, f'Cena', new_y='LAST', align='R', fill=1)
    pdf.cell(20,4, f'Popust', new_y='LAST', align='R', fill=1)
    pdf.cell(25,4, f'Iznos bez PDV', new_y='LAST', align='R', fill=1)
    pdf.cell(20,4, f'PDV stopa', new_x='LMARGIN', new_y='NEXT', align='R', fill=1)
    for item in bill.bill_items:
        print(f'item: {item=}')
        if item['sifra']:
            pdf.cell(55,4, f"({item['sifra']}) {item['naziv']}", new_y='LAST', align='L', border='B')
        else:
            pdf.cell(55,4, f"{item['naziv']}", new_y='LAST', align='L', border='B')
        pdf.cell(20,4, f'{item["kolicina"]}', new_y='LAST', align='R', border='B')
        pdf.cell(25,4, f'{item["jedinica_mere"]}', new_y='LAST', align='R', border='B')
        pdf.cell(25,4, "{:,.2f}".format(float(item["cena"])).replace(",", " ").replace(".", ",").replace(" ", "."), new_y='LAST', align='R', border='B') #"{:,.2f}".format(item["cena"]).replace(",", " ").replace(".", ",").replace(" ", ".")
        pdf.cell(20,4, f'{item["popust"]}%', new_y='LAST', align='R', border='B')
        pdf.cell(25,4, "{:,.2f}".format(float(item["iznos_bez_pdv"])).replace(",", " ").replace(".", ",").replace(" ", "."), new_y='LAST', align='R', border='B')     # item["iznos_bez_pdv"]
        pdf.cell(20,4, f'{item["pdv"]}%', new_x='LMARGIN', new_y='NEXT', align='R', border='B')     # item["pdv"]
    pdf.cell(0,6, f'', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.set_x(75)  # Prilagodite X poziciju prema potrebi
    pdf.cell(90,6, f'Zbir stavki - Nije predmet oporezivanja PDV:', new_y='LAST', align='R', border='B')
    pdf.cell(35,6, "{:,.2f}".format(bill.total_price).replace(",", " ").replace(".", ",").replace(" ", "."), new_y='NEXT', align='R', border='B')
    pdf.set_x(75)  # Prilagodite X poziciju prema potrebi
    pdf.cell(90,6, f'Ukupna osnovica - nije predmet oporezivanja PDV:', new_y='LAST', align='R')
    pdf.cell(35,6, "{:,.2f}".format(bill.total_price).replace(",", " ").replace(".", ",").replace(" ", "."), new_y='NEXT', align='R')
    pdf.set_x(75)  # Prilagodite X poziciju prema potrebi
    pdf.cell(90,6, f'Umanjena osnovica - nije predmet oporezivanja PDV:', new_y='LAST', align='R')
    pdf.cell(35,6, "{:,.2f}".format(bill.total_price).replace(",", " ").replace(".", ",").replace(" ", "."), new_y='NEXT', align='R')
    pdf.set_x(75)  # Prilagodite X poziciju prema potrebi
    pdf.set_font('DejaVuSansCondensed', 'B', 10)
    pdf.cell(90,6, f'Ukupno za uplatu:', new_y='LAST', align='R')
    pdf.cell(35,6, "{:,.2f}".format(bill.total_price).replace(",", " ").replace(".", ",").replace(" ", "."), new_y='NEXT', align='R')
    
    
    path = "kpo/static/bills_data/"
    file_name = f'{bill.bill_number}_{bill.id}.pdf'
    pdf.output(path + file_name)
    return file_name


def bill_list_gen(bills, customer, start_date, end_date):
    bill = bills[0]
    print(f'bill: {bill=}')
    company_logo = 'kpo/static/company_logos/' + bill.bill_company.company_logo
    company_name = bill.bill_company.companyname
    company_city = bill.bill_company.company_city
    company_mail = bill.bill_company.company_mail
    company_phone = bill.bill_company.company_phone
    company_site = bill.bill_company.company_site
    print(f'{company_logo=}')
    print(f'{company_name=}')
    print(f'{company_city=}')
    print(f'{company_mail=}')
    print(f'{company_phone=}')
    print(f'{company_site=}')
    class PDF(FPDF):
        def __init__(self, **kwargs):
            super(PDF, self).__init__(**kwargs)
            self.add_font('DejaVuSansCondensed', '', './kpo/static/fonts/DejaVuSansCondensed.ttf', uni=True)
            self.add_font('DejaVuSansCondensed', 'B', './kpo/static/fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
        def header(self):
            # Logo
            self.image(company_logo, 180, 5, 25)
            self.set_font('DejaVuSansCondensed', 'B', 12)
            self.multi_cell(0, 8, f'Izvod faktura za klijenta {customer.customer_name}:\r\nPeriod od {datetime.strptime(start_date, "%Y-%m-%d").strftime("%d.%m.%Y.")} do {datetime.strptime(end_date, "%Y-%m-%d").strftime("%d.%m.%Y.")}', new_y='NEXT', new_x='LMARGIN')
            
            self.set_y(30)
            self.set_font('DejaVuSansCondensed', 'B', 8)
            self.set_fill_color(192, 192, 192)
            self.cell(25, 8, f'Broj fakture', new_y='LAST', align='C', border = 1, fill=True)
            self.cell(30, 8, f'Datum prometa', new_y='LAST', align='C', border = 1, fill=True)
            self.cell(30, 8, f'Datum dospeća', new_y='LAST', align='C', border = 1, fill=True)
            self.cell(35, 8, f'Iznos', new_y='LAST', align='C', border = 1, fill=True)
            self.cell(35, 8, f'Uplaćeno', new_y='LAST', align='C', border = 1, fill=True)
            self.cell(35, 8, f'Preostalo za uplatu', new_y='NEXT', new_x='LMARGIN', align='C', border = 1, fill=True)
            self.set_font('DejaVuSansCondensed', '', 8)
        def footer(self):
            # Postavljanje fonta
            self.set_font('DejaVuSansCondensed', '', 8)
            
            # Računanje Y pozicije za footer
            page_height = self.h  # Dobavljanje visine stranice
            footer_height = 10  # Visina footera (u mm)
            footer_ypos = page_height - footer_height - 10  # Izračunavanje Y pozicije

            # Postavljanje pozicije za centriranje teksta
            self.set_y(footer_ypos + (footer_height - self.font_size) / 2)

            # Footer tekst
            footer_text = f'{company_name} | {company_city} | {company_mail} | {company_phone} | {company_site}'
            self.cell(0, footer_height, footer_text, ln=True, align='C')
            self.cell(0, 3, f'{self.page_no()}/{self.page_no()}', align='R')
    
    pdf=PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    total_price = 0
    total_payments = 0
    for bill in bills:
        pdf.cell(25, 8, f'{bill.bill_number}', new_y='LAST', align='C', border = 1)
        pdf.cell(30, 8, f'{bill.bill_transaction_date.strftime("%d.%m.%Y.")}', new_y='LAST', align='C', border = 1)
        pdf.cell(30, 8, f'{bill.bill_due_date.strftime("%d.%m.%Y.")}', new_y='LAST', align='C', border = 1)
        pdf.cell(35, 8, f'{bill.total_price:.2f}', new_y='LAST', align='R', border = 1)
        pdf.cell(35, 8, f'{bill.total_payments:.2f}', new_y='LAST', align='R', border = 1)
        pdf.cell(35, 8, f'{(bill.total_price - bill.total_payments):.2f}', new_y='NEXT', new_x='LMARGIN', align='R', border = 1)
        total_price += bill.total_price
        total_payments += bill.total_payments
    pdf.line(10, pdf.get_y() +10, 200, pdf.get_y()+ 10)
    pdf.set_y(pdf.get_y() + 10)
    pdf.cell(0, 8, f'Ukupno: {total_price:.2f} | Uplaćeno: {total_payments:.2f} | Preostalo: {(total_price - total_payments):.2f}', new_y='NEXT', new_x='LMARGIN', align='R')
    
    path = "kpo/static/bills_data/"
    file_name = f'export.pdf'
    pdf.output(path + file_name)
    return file_name