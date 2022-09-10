from datetime import date
from dateutil.relativedelta import relativedelta


class Data():
    def __init__(self):
        self.limit = 6000000
        self.start_day = date.today()
        self.end_day = []
        self.razlika = []
        list = [0, 1, 7, 15, 30, 90] # broj dana za proračun do limita
        for item in list:
            self.end_day.append(date.today() + relativedelta(days=item) + relativedelta(days=-365))

    def razlika(self):
        for value in range(6):
            self.razlika.append(self.limit - Invoice.query.with_entities(
                        func.sum(Invoice.amount).label("suma")
                        ).filter(Invoice.date.between(self.start_day, self.end_day[value])).filter_by(
                        company_id=2
                        ).first()[0])
        return self.razlika

form = Data()
form.razlika()
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
