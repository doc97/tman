from flask import render_template, redirect, url_for
from flask_login import login_required
from application import app
from application.tasks.models import Tag

import application.session_state as state


@app.route('/tags/all')
@login_required
def tags_all():
    if not state.validate():
        state.save('next', 'tags_all')
        return redirect(url_for('auth_logout'))
    state.save('url_function', 'tags_all')
    tags = Tag.query.all()
    return render_template('tags/tags_all.html', tags=tags)
