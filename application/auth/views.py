from flask import render_template, request, redirect, session, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db
from application.auth.models import Account
from application.auth.forms import LoginForm, RegistrationForm

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

import application.tasks.session_state as state
import application.tasks.functions as func


ph = PasswordHasher()


@app.route('/auth/register', methods=['GET', 'POST'])
def auth_register():
    if request.method == 'GET':
        return render_template('auth/register.html', form=RegistrationForm())

    form = RegistrationForm(request.form)
    if not form.validate():
        return render_template('auth/register.html', form=form)

    result = Account.query.filter(Account.username == form.username.data).first()
    if not result:
        # argon2 includes the generated salt into the hash
        # no need to supply it yourself
        pw_hash = ph.hash(form.password.data)

        new_account = Account(username=form.username.data, password=pw_hash)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('auth_login'))

    return render_template('auth/register.html', form=form, registration_error='Username is already in use')


@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('tasks_today'))
        return render_template('auth/login.html', form=LoginForm())

    form = LoginForm(request.form)
    if not form.validate():
        return render_template('auth/login.html', form=form)

    result = Account.query.filter(Account.username == form.username.data).first()
    if result:
        try:
            ph.verify(result.password, form.password.data)
            login_user(result, remember=form.remember.data)

            state.initialize()
            func.normalize_tasklist_ordering(1)
            func.normalize_tasklist_ordering(2)
            func.normalize_tasklist_ordering(3)
            if 'next' in session:
                return redirect(session['next'])
            return redirect(url_for('tasks_today'))
        except VerifyMismatchError:
            error_msg = 'No such username or password'
        except VerificationError:
            error_msg = 'Something went wrong, try again.'
    else:
        error_msg = 'No such username or password'

    return render_template('auth/login.html', form=form, login_error=error_msg)


@app.route('/auth/logout')
def auth_logout():
    session['__invalidate__'] = True
    logout_user()
    return redirect(url_for('auth_login'))
