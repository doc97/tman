from flask_login import login_required
from flask import render_template, request, redirect, url_for, jsonify
from application import app, db
from application.tags.models import Tag

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


@app.route('/tags/delete', methods=['POST'])
@login_required
def delete_tag():
    if not state.validate():
        state.save('next', 'tags_all')
        return redirect(url_for('auth_logout'))

    json_id_data = request.json['tag_id'] if 'tag_id' in request.json else ''
    tag_id = int(json_id_data[4:]) if json_id_data.startswith('tag-') else -1
    tag = Tag.query.filter((Tag.id == tag_id) & (Tag.account_id == current_user.id)).first()
    if tag:
        db.session.delete(tag)
        db.session.commit()
    return state.get_url_for_function()


@app.route('/tags/query', methods=['POST'])
@login_required
def query_all_tags():
    if not state.validate():
        state.save('next', 'tasks_today')
        return redirect(url_for('auth_logout'))

    tag_query = Tag.query.all()
    tags = []
    for tag in tag_query:
        tags.append({"id": tag.id, "name": tag.name})

    return jsonify(tags)
