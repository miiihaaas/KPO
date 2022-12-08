from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Blueprint
from flask import  render_template, redirect, url_for, flash
from sqlalchemy import func
from kpo.models import Invoice
from kpo.invoices.forms import DashboardData
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        form = DashboardData(current_user.user_company.id)
        print(f'{current_user.user_company.id=}')
    else:
        print(f'nije ulogovan niko')
        flash('Morate da budete prijavljeni da bi ste pristupili ovoj stranici.' 'info')
        return redirect(url_for('main.about'))
    return render_template('home.html', title='Početna', form=form)

    print(form.start_day)


@main.route("/about")
def about():
    return render_template('about.html', title='O softveru')
