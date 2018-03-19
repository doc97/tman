from flask import flash, render_template, request, redirect, session, url_for
from application import app, db
from application.tasks.models import Account, Category, TaskList, Task
from argon2 import PasswordHasher
import os

ph = PasswordHasher()

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('home.html', categories=Category.query.all())

@app.route('/register', methods=['GET', 'POST'])
def register():
    session['logged_in'] = False
    if request.method == 'POST':
        form_user = request.form['username']
        form_passwd = request.form['password']
        query = Account.query.filter(Account.username == form_user)
        result = query.first()
        if not result:
            # argon2 includes the generated salt into the hash
            # no need to supply it yourself
            pw_hash = ph.hash(form_passwd)

            create_record = Account(username=request.form['username'], password=pw_hash)
            db.session.add(create_record)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash('Username is already in use!')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_user = request.form['username']
        form_passwd = request.form['password']

        query = Account.query.filter(Account.username == form_user)
        result = query.first()

        if result:
            db_passwd = result.password

            try:
                ph.verify(db_passwd, form_passwd)
                session['logged_in'] = True
                return redirect(url_for('index'))
            except:
                pass

        flash('Wrong username or password!')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))
