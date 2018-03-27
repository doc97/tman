from flask import render_template, request, redirect, session, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import Account
from application.auth.forms import LoginForm, RegistrationForm
from argon2 import PasswordHasher

ph = PasswordHasher()

@app.route('/auth/register', methods=['GET', 'POST'])
def auth_register():
    session.pop('account_id', None)
    if request.method == 'GET':
        return render_template('auth/register.html', form = RegistrationForm())

    form = RegistrationForm(request.form)
    if not form.validate():
        return render_template('auth/register.html', form = form)

    result = Account.query.filter(Account.username == form.username.data).first()
    if not result:
        # argon2 includes the generated salt into the hash
        # no need to supply it yourself
        pw_hash = ph.hash(form.password.data)

        new_account = Account(username=form.username.data, password=pw_hash)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('auth_login'))

    return render_template('auth/register.html', form = form, registration_error = 'Username is already in use')

@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'GET':
        return render_template('auth/login.html', form = LoginForm())

    form = LoginForm(request.form)
    if not form.validate():
        return render_template('auth/login.html', form = form)

    result = Account.query.filter(Account.username == form.username.data).first()
    if result:
        db_passwd = result.password
        try:
            ph.verify(db_passwd, form.password.data)
            session['account_id'] = result.id
            login_user(result)
            return redirect(url_for('index'))
        except:
            return "Wrong password"
            pass

    return render_template('auth/login.html', form = form, login_error = 'No such username or password')

@app.route('/auth/logout')
def auth_logout():
    session.pop('account_id', None)
    session['__invalidate__'] = True
    logout_user()
    return redirect(url_for('auth_login'))
