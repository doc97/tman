from flask import render_template, request, redirect, session, url_for

from application import app, db
from application.auth.models import Account
from application.auth.forms import LoginForm, RegistrationForm
from argon2 import PasswordHasher

ph = PasswordHasher()

@app.route('/auth/register', methods=['GET', 'POST'])
def auth_register():
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
        if 'account_id' in session:
            return redirect_next()
        return render_template('auth/login.html', form = LoginForm())

    form = LoginForm(request.form)
    if not form.validate():
        return render_template('auth/login.html', form = form)

    result = Account.query.filter(Account.username == form.username.data).first()
    if result:
        try:
            ph.verify(result.password, form.password.data)
            session['account_id'] = result.id
            return redirect_next()
        except:
            pass

    return render_template('auth/login.html', form = form, login_error = 'No such username or password')

@app.route('/auth/logout')
def auth_logout():
    session.pop('account_id', None)
    session['__invalidate__'] = True
    return redirect(url_for('auth_login'))

def redirect_next():
    if 'next' in session:
        next_view = url_for(session.get('next'))
        session.pop('next', None)
    else:
        next_view = url_for('tasks_today')
    return redirect(next_view)
