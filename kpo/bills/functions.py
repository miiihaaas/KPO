from fpdf import FPDF


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
    pdf.cell(35,6, f'proračun', new_y='NEXT', align='R')
    pdf.set_x(75)  # Prilagodite X poziciju prema potrebi
    pdf.cell(90,6, f'Umanjena osnovica - nije predmet oporezivanja PDV:', new_y='LAST', align='R')
    pdf.cell(35,6, f'proračun', new_y='NEXT', align='R')
    pdf.set_x(75)  # Prilagodite X poziciju prema potrebi
    pdf.set_font('DejaVuSansCondensed', 'B', 10)
    pdf.cell(90,6, f'Ukupno za uplatu:', new_y='LAST', align='R')
    pdf.cell(35,6, f'proračun', new_y='NEXT', align='R')
    
    
    path = "kpo/static/bills_data/"
    file_name = f'{bill.bill_number}_{bill.id}.pdf'
    pdf.output(path + file_name)
    return file_name


def bill_list_gen(bills):
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