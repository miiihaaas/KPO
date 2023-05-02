from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from kpo import db, app
from kpo.models import Bill
from kpo.bills.forms import RegisterBillForm


bills = Blueprint('bills', __name__)


@bills.route("/bill_list")
def bill_list():
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    # bills = Bill.query.all()
    return render_template('bill_list.html', title='Lista faktura', bills=bills)


@bills.route("/register_b",  methods=['GET', 'POST'])
def register_b():
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da biste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    form = RegisterBillForm()
    return render_template('register_b.html', title='Registracija nove fakture', form=form)
    