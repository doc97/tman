from flask import render_template, redirect, session, url_for
from application import app


@app.after_request
def remove_if_invalid(response):
    if '__invalidate__' in session:
        response.delete_cookie(app.session_cookie_name)
    return response


@app.route('/')
def index():
    if not session.get('account_id'):
        return render_template('index.html')
    else:
        return redirect(url_for('tasks_today'))
