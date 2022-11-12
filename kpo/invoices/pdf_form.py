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
    class PDF(FPDF):
        def header(self):
            self.set_font('times', 'I', 8)
            self.cell(8, 3, f'header', ln=True, align='L')
    pdf=PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('times','B', 16)
    pdf.cell(0, 30, f'izvoz KPO podataka', ln=True, align='C')
    pdf.set_font('times','B', 12)
    pdf.cell(50, 10, f'Od: {start}', ln=False, align='L')
    pdf.cell(50, 10, f'Do: {end}', ln=True, align='L')

    ukupno = 0
    for invoice in filtered_invoices:
        if invoice.cancelled == False:
            ukupno = ukupno + invoice.amount
            pdf.set_font('times','B', 10)
            pdf.cell(20, 5, f'{replace_serbian_characters(invoice.date)}', border=1, ln=False, align='C')
            pdf.cell(20, 5, f'{replace_serbian_characters(invoice.invoice_number)}', border=1, ln=False, align='C')
            pdf.cell(50, 5, f'{replace_serbian_characters(invoice.customer)}', border=1, ln=False, align='C')
            pdf.cell(50, 5, f'{replace_serbian_characters(invoice.service)}', border=1, ln=False, align='C')
            pdf.cell(30, 5, f'{replace_serbian_characters(invoice.amount)}', border=1, ln=True, align='R')

    pdf.cell(30, 5, f'Ukupno: {ukupno}')

    path = "kpo/static/pdf_forms/"
    pdf.output(path + file_name)
