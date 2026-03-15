import pandas as pd
from kpo.models import Invoice, User, Company
from kpo import db

x = input('da li žeiš da masovno uneseš fakture iz exel fajla? (y/n)')
if x=="y":
    df = pd.read_excel('D:\Mihas\Programming\Python\Projects\KPO\data.xlsx', sheet_name='pripremljen 2021 2022')

    for index, row in df.iterrows():
        invoice_input = Invoice(
                        date=row['Datum'],
                        invoice_number=row['Broj fakture'],
                        customer=row['Kupac'],
                        service=row['Usluga'],
                        amount=row['Iznos fakture'],
                        company_id=2,
                        user_id=2,
                        cancelled=False)
        print(invoice_input)
        db.session.add(invoice_input)
        db.session.commit()


x = input('da li žeiš da masovno uneseš korisnike iz exel fajla? (y/n)')
if x=="y":
    df = pd.read_excel('D:\Mihas\Programming\Python\Projects\KPO\data.xlsx', sheet_name='Users')

    for index, row in df.iterrows():
        user_input = User(id=row['id'], email=row['email'], password=row['password'], name=row['name'], surname=row['surname'], workplace=row['workplace'], authorization=row['authorization'], gender=row['gender'], company_id=row['company_id'])
        print(user_input)
        db.session.add(user_input)
        db.session.commit()


x = input('da li žeiš da masovno uneseš kompanije iz exel fajla? (y/n)')
if x=="y":
    df = pd.read_excel('D:\Mihas\Programming\Python\Projects\KPO\data.xlsx', sheet_name='Companys')

    for index, row in df.iterrows():
        company_input = Company(id=row['id'], companyname=row['companyname'], company_address=row['company_address'], company_address_number=row['company_address_number'], company_zip_code=row['company_zip_code'], company_city=row['company_city'], company_state=row['company_state'], company_pib=row['company_pib'], company_mb=row['company_mb'], company_site=row['company_site'], company_mail=row['company_mail'], company_phone=row['company_phone'], company_logo=row['company_logo'])
        print(company_input)
        db.session.add(company_input)
        db.session.commit()
