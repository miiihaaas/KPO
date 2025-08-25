from fpdf import FPDF
from datetime import datetime
import os
from kpo import logger

def generate_kpo_book(bills, date_from, date_to):
    """
    Generiše KPO knjigu za date fakture u datom periodu.
    
    Args:
        bills: Lista faktura za prikaz
        date_from: Početni datum perioda
        date_to: Krajnji datum perioda
    
    Returns:
        Naziv generisanog PDF fajla
    """
    logger.info(f'Generisanje KPO knjige za period od {date_from} do {date_to}')
    
    if not bills:
        logger.error("Nema faktura za prikaz u KPO knjizi")
        return None
    
    # Uzimamo prvi račun za informacije o kompaniji
    bill = bills[0]
    company_logo = 'kpo/static/company_logos/' + bill.bill_company.company_logo
    company_name = bill.bill_company.companyname
    company_address = bill.bill_company.company_address
    company_address_number = bill.bill_company.company_address_number
    company_zip_code = bill.bill_company.company_zip_code
    company_city = bill.bill_company.company_city
    company_state = bill.bill_company.company_state
    company_pib = bill.bill_company.company_pib
    company_mb = bill.bill_company.company_mb
    company_mail = bill.bill_company.company_mail
    company_site = bill.bill_company.company_site
    company_phone = bill.bill_company.company_phone
    
    class PDF(FPDF):
        def __init__(self, **kwargs):
            super(PDF, self).__init__(**kwargs)
            self.add_font('DejaVuSansCondensed', '', './kpo/static/fonts/DejaVuSansCondensed.ttf', uni=True)
            self.add_font('DejaVuSansCondensed', 'B', './kpo/static/fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
            # Za proveru da li je stranica poslednja
            self.is_last_page = False
            
        def header(self):
            # Logo
            self.image(company_logo, 10, 10, 25)
            # Podaci o firmi
            self.set_font('DejaVuSansCondensed', '', 10)
            self.cell(60, 5, f"Studio {company_name}", new_x="RIGHT", new_y="LAST")
            self.cell(70, 5, f"PIB: {company_pib}", new_x="RIGHT", new_y="LAST")
            self.cell(60, 5, f"web: {company_site}", new_x="LMARGIN", new_y="NEXT")
            
            self.cell(60, 5, f"{company_address} {company_address_number}", new_x="RIGHT", new_y="LAST")
            self.cell(70, 5, f"MB: {company_mb}", new_x="RIGHT", new_y="LAST")
            self.cell(60, 5, f"email: {company_mail}", new_x="LMARGIN", new_y="NEXT")
            
            self.cell(60, 5, f"{company_zip_code} {company_city}", new_x="RIGHT", new_y="LAST")
            self.cell(70, 5, "", new_x="RIGHT", new_y="LAST")
            self.cell(60, 5, f"tel: {company_phone}", new_x="LMARGIN", new_y="NEXT")
            
            self.cell(60, 5, f"{company_state}", new_x="LMARGIN", new_y="NEXT")
            
            # Linija ispod zaglavlja
            self.line(10, 30, 200, 30)
            
            # Naslov
            self.set_y(40)
            self.set_font('DejaVuSansCondensed', 'B', 16)
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            self.cell(0, 10, f"Izvoz KPO podataka za period: {date_from_obj.strftime('%Y-%m-%d')} - {date_to_obj.strftime('%Y-%m-%d')}", new_x="LMARGIN", new_y="NEXT", align="C")
            
            # Zaglavlja tabele
            self.set_font('DejaVuSansCondensed', 'B', 8)
            self.set_fill_color(240, 240, 240)
            self.cell(20, 8, "Datum", new_x="RIGHT", new_y="LAST", border=1, align="C", fill=True)
            self.cell(20, 8, "Br. fakture", new_x="RIGHT", new_y="LAST", border=1, align="C", fill=True)
            self.cell(70, 8, "Klijent", new_x="RIGHT", new_y="LAST", border=1, align="C", fill=True)
            self.cell(55, 8, "Opis Knjiženja", new_x="RIGHT", new_y="LAST", border=1, align="C", fill=True)
            self.cell(25, 8, "Iznos [rsd]", new_x="LMARGIN", new_y="NEXT", border=1, align="C", fill=True)
        
        def footer(self):
            # Postavljanje fonta
            self.set_font('DejaVuSansCondensed', '', 8)
            
            # Broj stranice u formatu n/ukupno
            self.set_y(-10)
            # Koristi specijalne makroe {nb} i {p} koje fpdf2 zamenjuje sa brojem stranica
            page_text = f"{self.page_no()}/{{nb}}"
            self.cell(0, 10, page_text, new_x="LMARGIN", new_y="NEXT", align="R")
            
            # Samo ako je poslednja stranica, dodaj potpis
            if self.is_last_page:
                self.set_y(-25)  # Malo više za potpis
                self.cell(0, 10, "Potpis ovlašćenog lica:", new_x="LMARGIN", new_y="NEXT", align="R")
                
                # Linija za potpis odmah ispod teksta
                signature_line_y = self.get_y() + 2  # Malo ispod teksta
                signature_line_start_x = self.w - 70  # 70mm od desne ivice
                signature_line_end_x = self.w - 10   # 10mm od desne ivice
                self.line(signature_line_start_x, signature_line_y, signature_line_end_x, signature_line_y)
    
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Postavljanje fonta za podatke
    pdf.set_font('DejaVuSansCondensed', '', 8)
    
    # Ukupan iznos za sve fakture
    total_amount = 0
    
    for bill in bills:
        # Formatiranje datuma
        if bill.bill_transaction_date:
            transaction_date = bill.bill_transaction_date.strftime("%Y-%m-%d")
        else:
            transaction_date = ""
        
        # Ispis podataka o fakturi
        pdf.cell(20, 6, transaction_date, new_x="RIGHT", new_y="LAST", border=1, align="C")
        pdf.cell(20, 6, bill.bill_number, new_x="RIGHT", new_y="LAST", border=1, align="C")
        pdf.cell(70, 6, bill.bill_customer.customer_name, new_x="RIGHT", new_y="LAST", border=1)
        
        # Opis knjiženja
        if "veb" in bill.bill_service.lower() or "web" in bill.bill_service.lower():
            opis = "Održavanje veb sajta"
        elif "soft" in bill.bill_service.lower():
            opis = "Održavanje softvera"
        elif "izrad" in bill.bill_service.lower():
            opis = "Izrada veb sajta"
        elif "program" in bill.bill_service.lower():
            opis = "Programerske usluge"
        elif "host" in bill.bill_service.lower():
            opis = "Hosting i domen"
        else:
            opis = bill.bill_service[:50] if bill.bill_service else "Održavanje veb sajta"
        
        pdf.cell(55, 6, opis, new_x="RIGHT", new_y="LAST", border=1)
        
        # Iznos
        pdf.cell(25, 6, f"{bill.total_price:.2f}", new_x="LMARGIN", new_y="NEXT", border=1, align="R")
        
        # Dodavanje iznosa ukupnoj sumi
        total_amount += bill.total_price
    
    # Ispis ukupnog iznosa na kraju tabele
    pdf.set_font('DejaVuSansCondensed', 'B', 9)
    pdf.cell(165, 8, "Ukupno:", new_x="RIGHT", new_y="LAST", border=1, align="R")
    pdf.cell(25, 8, f"{total_amount:.2f} rsd", new_x="LMARGIN", new_y="NEXT", border=1, align="R")
    
    # Označimo da je poslednja stranica
    pdf.is_last_page = True
    
    # Generisanje PDF-a
    path = "kpo/static/bills_data/"
    file_name = f'kpo_book_{date_from}_{date_to}.pdf'
    pdf.output(path + file_name)
    return file_name
