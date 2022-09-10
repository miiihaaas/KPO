from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Blueprint
from flask import  render_template, redirect, url_for, flash
from sqlalchemy import func
from kpo.models import Invoice
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    # fakturisano u tekućoj godini
    # fakturisano u poslednjih godinu dana

    #danas do limita je preostalo: ___                  0
    #sutra do limita je preostalo: ___                  1
    #za 7 dana do limita je preostalo: ___              7
    # za 15 dana do limita je preostalo: ___            15
    #za mesec dana do limita je preostalo: ___          30
    #za 3 meseca do limita je preostalo: ___            90
    class DashboardData():
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


# func.sum(func.IF(
#             Invoice.paidtodate>0,
#             Invoice.paidtodate
#             )
#         ).label("amount")


    if current_user.is_authenticated:
        form = DashboardData(current_user.user_company.id)
    else:
        print(f'nije ulogovan niko')
        return redirect(url_for('main.about'))
        flash('You have to be logged in to visit Home page' 'info')
    return render_template('home.html', title='Home', form=form)

    print(form.start_day)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
