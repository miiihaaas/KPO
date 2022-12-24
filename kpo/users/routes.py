from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort
from kpo import db, bcrypt, mail
from kpo.users.forms import RegistrationUserForm, LoginForm, UpdateUserForm, RequestResetForm, ResetPasswordForm
from kpo.models import Company, User
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from wtforms.validators import ValidationError


users = Blueprint('users', __name__)


@users.route("/user_list")
def user_list():
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da bi ste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    users = User.query.all()
    return render_template('user_list.html', title='Korisnici', users=users)


@users.route("/register_u", methods=['GET', 'POST'])
# @login_required
def register_u():
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da bi ste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.is_authenticated and (current_user.authorization != 'c_admin' and current_user.authorization != 's_admin'):
        flash('Nemate autorizaciju da pristupite ovoj stranici', 'danger')
        return redirect(url_for('main.home'))
    form = RegistrationUserForm()
    form.reset()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if current_user.authorization == 'c_admin':
            user = User(email=form.email.data,
                        password=hashed_password,
                        name=form.name.data,
                        surname=form.surname.data,
                        workplace=form.workplace.data,
                        authorization=form.authorization.data,
                        gender=form.gender.data,
                        company_id=Company.query.filter_by(companyname=current_user.user_company.companyname).first().id) #Company.query.filter_by(companyname=form.company_id.data).first().id) #int(current_user.company_id)) ##
        elif current_user.authorization == 's_admin':
            user = User(email=form.email.data,
                        password=hashed_password,
                        name=form.name.data,
                        surname=form.surname.data,
                        workplace=form.workplace.data,
                        authorization=form.authorization.data,
                        gender=form.gender.data,
                        company_id=form.company_id.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Kreiran je porfil: {form.name.data} {form.surname.data}!', 'success')
        return redirect(url_for('users.user_list'))
    return render_template('register_u.html', title='Registracija novog korisnika', form=form, legend='Dodavanje novog korisnika')




@users.route("/user/<int:user_id>", methods=['GET', 'POST'])
# @login_required
def user_profile(user_id): #ovo je funkcija za editovanje user-a
    user = User.query.get_or_404(user_id)
    if not current_user.is_authenticated:
        flash('Morate da budete prijavljeni da bi ste pristupili ovoj stranici.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization != 's_admin' and current_user.authorization != 'c_admin':
        if current_user.id != user.id:
            abort(403)
    elif current_user.authorization == 's_admin':
        pass
    elif current_user.user_company.id != user.user_company.id:
        abort(403)

    form = UpdateUserForm()
    form.reset()

    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.workplace = form.workplace.data

        if user.email == form.email.data:
            user.email = form.email.data
        else:
            validate_email = User.query.filter_by(email=form.email.data).first()
            if validate_email:
                flash('Taj mejl je zauzet, molim Vas izaberite drugi mejl.', 'danger')
                return render_template('user.html', title="Izmena korisničkih podataka", user=user, form=form, legend='Edit User')
            else:
                user.email = form.email.data

        if current_user.authorization != 's_admin':
            user.authorization = user.authorization
        else:
            user.authorization = form.authorization.data

        user.gender = form.gender.data

        if current_user.authorization == 's_admin':
            user.company_id = form.company_id.data
        else:
            user.company_id = user.company_id

        db.session.commit()
        flash('Profil je ažuriran', 'success')
        return redirect(url_for('users.user_list'))
    elif request.method == 'GET':
        form.name.data = user.name
        form.surname.data = user.surname
        form.workplace.data = user.workplace
        form.email.data = user.email

        form.authorization.choices = [('c_user', 'USER'),('c_admin', 'ADMIN')]
        form.authorization.data = user.authorization

        form.gender.choices = [(1, 'MUŠKI'),(2, 'ŽENSKI')]
        form.gender.data = user.gender

        form.company_id.choices = [(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()]
        form.company_id.data = str(user.company_id)
    return render_template('user.html', title="Izmena korisničkih podataka", user=user, form=form, legend='Izmena korisničkih podataka')



@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Dobrodošli {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Korisničko ime ili lozinka nisu ispravni!', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/user/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if not current_user.is_authenticated:
        flash('Morate da budete ulogovani da bi ste pristupili ovoj stranici', 'danger')
        return redirect(url_for('users.login'))
    elif not bcrypt.check_password_hash(current_user.password, request.form.get("input_password")):
        print('nije dobar password')
        abort(403)
    else:
        if current_user.authorization == 'c_user':
            abort(403)
        elif current_user.authorization == 'c_admin':
            if current_user.user_company.id != user.user_company.id:
                abort(403)
            db.session.delete(user)
            db.session.commit()
            flash(f'Profil korisnika {user.name} {user.surname} je izbrisan', 'success' )
            return redirect(url_for('users.user_list'))
        else:
            db.session.delete(user)
            db.session.commit()
            flash(f'profil korisnika {user.name} {user.surname} je izbrisan', 'success' )
            return redirect(url_for('users.user_list'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Zahtev za resetovanje lozinke', sender='noreplay@kpo.digital', recipients=[user.email])
    msg.body = f'''Da biste resetovali lozinku, kliknite na sledeći link:
{url_for('users.reset_token', token=token, _external=True)}

Ako Vi niste napavili ovaj zahtev, molim Vas ignorišite ovaj mejl i neće biti napravljene nikakve izmene na Vašem nalogu.
    '''
    mail.send(msg)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user  = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Mejl je poslat na Vašu adresu sa instrukcijama za resetovanje lozinke. ', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Resetovanje lozinke', form=form, legend='Resetovanje lozinke')


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        user = User.verify_reset_token(token)
        if user is None:
            flash('Ovo je nevažeći ili istekli token.', 'warning')
            return redirect(url_for('users.reset_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash(f'Vaša lozinka je ažurirana!', 'success')
            return redirect(url_for('users.login'))
        return render_template('reset_token.html', title='Resetovanje lozinke', form=form)
