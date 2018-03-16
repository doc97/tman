from flask import Flask, escape, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = '\xb1CL\xc7,\x90/C=\xc0\x1a\xec\xee\x14q\xf1\x91%Oh\xcc\x89\x8f&'

# Page / view methods
@app.route('/')
def page_index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def page_login():
    error = None
    if request.method == 'POST':
        if validate_user(request.form['username'], request.form['password']):
            return login(request.form['username'])
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

@app.route('/logout')
def page_logout():
    session.pop('username', None)
    return redirect(url_for('page_index'))

# Data model methods
def validate_user(username, password):
    return True

def login(username):
    session['username'] = username
    flash('You were successfully logged in as \'%s\'' % username)
    return redirect(url_for('page_index'))
