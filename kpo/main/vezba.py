from datetime import date
from dateutil.relativedelta import relativedelta
# from kpo.models import Invoice


class Data():
    def __init__(self, company_id):
        self.limit = 6000000
        self.end_day = date.today()
        self.start_day = [date(date.today().year, 1, 1)]
        self.razlika = []
        self.company_id = company_id
        list = [0, 1, 7, 15, 30, 90] # broj dana za proračun do limita
        for item in list:
            self.start_day.append(date.today() + relativedelta(days=item) + relativedelta(days=-365))

        for value in range(7):
            try:
                self.razlika.append(self.limit + 2000000 - Invoice.query.with_entities(
                            func.sum(Invoice.amount).label("suma")
                            ).filter(Invoice.date.between(self.start_day[value], self.end_day)).filter_by(
                            company_id=self.company_id
                            ).first()[0])

            except TypeError:
                self.razlika = [0, 0, 0, 0, 0, 0, 0]

form = Data(2)
print(form.razlika)

# class Sabiranje:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#
#     def sabiranje_dva_broja(self):
#         c = self.a + self.b
#         return c
#
# form=Sabiranje(15, 34)
# print(form)
# print(form.a)
# print(type(form.a))
# print(form.b)
# print(type(form.b))
#
# print(form.a + form.b)
#
# p=form.sabiranje_dva_broja()
# print(p)
#
#
# print("_______")
# start_day = []
# end_day = []
# list = [0, 1, 7, 15, 30, 90]
# for item in list:
#     start_day.append(date.today() + relativedelta(days=item))
#     end_day.append(date.today() + relativedelta(days=item) + relativedelta(days=-365))
#
# print(start_day)
# print(end_day)
