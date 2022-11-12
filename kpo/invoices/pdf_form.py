from fpdf import FPDF
import datetime


def replace_serbian_characters(string):
    # breakpoint()
    try:
        string = string.replace("č", "c")
    except:
        pass
    try:
        string = string.replace("ć", "c")
    except:
        pass
    try:
        string = string.replace("đ", "dj")
    except:
        pass
    try:
        string = string.replace("ž", "z")
    except:
        pass
    try:
        string = string.replace("š", "s")
    except:
        pass
    try:
        string = string.replace("Č", "C")
    except:
        pass
    try:
        string = string.replace("Ć", "C")
    except:
        pass
    try:
        string = string.replace("Đ", "Dj")
    except:
        pass
    try:
        string = string.replace("Ž", "Z")
    except:
        pass
    try:
        string = string.replace("Š", "S")
    except:
        pass
    return string


def create_invoice_report(start, end, filtered_invoices, file_name):
    company_logo = "kpo/static/company_logos/" + filtered_invoices[0].invoice_company.company_logo
    company_name = replace_serbian_characters(filtered_invoices[0].invoice_company.companyname)
    company_address = replace_serbian_characters(filtered_invoices[0].invoice_company.company_address) + f" {filtered_invoices[0].invoice_company.company_address_number}"
    company_zip_code = filtered_invoices[0].invoice_company.company_zip_code
    company_city = replace_serbian_characters(filtered_invoices[0].invoice_company.company_city)
    company_state = replace_serbian_characters(filtered_invoices[0].invoice_company.company_state)
    company_pib = filtered_invoices[0].invoice_company.company_pib
    company_mb = filtered_invoices[0].invoice_company.company_mb
    company_phone = filtered_invoices[0].invoice_company.company_phone
    company_mail = filtered_invoices[0].invoice_company.company_mail
    company_site = filtered_invoices[0].invoice_company.company_site
    class PDF(FPDF):
        def header(self):
            # Logo
            self.image(company_logo, 1, 1, 25)
            # set font
            self.set_font('times', 'I', 8)
            # Kompanija
            self.cell(50, 3, f'                         {company_name}', ln=False, align='L')
            # PIB
            self.cell(0, 3, f'                         PIB: {company_pib}', ln=False, align='L')
            # web stranica
            self.cell(1, 3, f'                         web: {company_site}', ln=True, align='R')
            # adresa
            self.cell(50, 3, f'                         {company_address}', ln=False, align='L')
            # MB
            self.cell(0, 3, f'                         MB: {company_mb}', ln=False, align='L')
            # email
            self.cell(1, 3, f'                         email: {company_mail}', ln=True, align='R')
            # mesto
            self.cell(0, 3, f'                         {company_zip_code} {company_city}', ln=False, align='L')
            # telefon
            self.cell(1, 3, f'                         tel: {company_phone}', ln=True, align='R')
            # Država
            self.cell(8, 3, f'                         {company_state}', ln=True, align='L')
            # linija
            pdf.set_font('times','B', 16)
            pdf.cell(0, 30, f'Izvoz KPO podataka za period: {start} - {end} ', ln=True, align='L')
            pdf.line(10, 30, 200, 30)
            pdf.set_font('times','B', 10)
            pdf.cell(20, 5, f'Datum', border=1, ln=False, align='C')
            pdf.cell(20, 5, f'Br. fakture', border=1, ln=False, align='C')
            pdf.cell(50, 5, f'Klijent', border=1, ln=False, align='C')
            pdf.cell(80, 5, f'Opis Knjizenja', border=1, ln=False, align='C')
            pdf.cell(20, 5, f'Iznos [rsd]', border=1, ln=True, align='R')
        def footer(self):
            pass
    pdf=PDF()
    pdf.alias_nb_pages()
    # pdf.set_top_margin(0)
    pdf.add_page()

    ukupno = 0

    for invoice in filtered_invoices:
        if invoice.cancelled == False:
            ukupno = ukupno + invoice.amount
            pdf.set_font('times','', 10)
            pdf.multi_cell(20, 5, f'{replace_serbian_characters(invoice.date)}', border='T', new_y='LAST', align='C')
            pdf.multi_cell(20, 5, f'{replace_serbian_characters(invoice.invoice_number)}', border='T', new_y='LAST', align='C')
            pdf.multi_cell(50, 5, f'{replace_serbian_characters(invoice.customer)}', border='T', new_y='LAST', align='L')
            pdf.multi_cell(80, 5, f'{replace_serbian_characters(invoice.service)}', border='T', new_y='LAST', align='L')
            pdf.multi_cell(20, 5, f'{replace_serbian_characters(invoice.amount)}', border='B', new_x='LMARGIN', new_y='NEXT', align='R')

    pdf.cell(0, 5, f'Ukupno: {round(ukupno,2)} rsd', border='T', align='R')

    path = "kpo/static/pdf_forms/"
    pdf.output(path + file_name)
