from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from application import app, db
from application.classes.tags.models import Tag
from application.classes.tags.forms import TagForm

import application.session_state as state


@app.route('/tags/all')
@login_required
def tags_all():
    if not state.validate():
        state.save('next', 'tags_all')
        return redirect(url_for('auth_logout'))
    state.save('url_function', 'tags_all')
    tags = Tag.query.filter(Tag.account_id == current_user.id).all()
    return render_template('tags/tags_all.html', tags=tags)


@app.route('/tags/edit', methods=['GET', 'POST'])
@login_required
def tags_edit():
    if not state.validate():
        state.save('next', 'tags_all')
        return redirect(url_for('auth_logout'))

    if request.method == "GET":
        state.save('url_function', 'tags_edit')

        tag_id_data = request.args.get("tag", default="", type=str)
        tag_id = tag_id_data[4:] if tag_id_data.startswith('tag-') else -1
        tag_query = Tag.query.filter((Tag.id == tag_id) & (Tag.account_id == current_user.id)).first()

        tag_form = TagForm()
        if tag_query:
            tag_form.name.data = tag_query.name
        return render_template('tags/tags_edit.html', form=tag_form, tag=tag_query)
    else:
        form = TagForm(request.form)

        if not form.validate():
            return redirect(state.get_url_for_function())

        form_name = form.name.data
        tag_id = request.args.get("tagId", default=-1, type=int)
        tag_query = Tag.query.filter((Tag.id == tag_id) & (Tag.account_id == current_user.id)).first()
        print(tag_query)

        if tag_query:
            tag_query.name = form_name
        else:
            created_tag = Tag(current_user.id, form_name)
            db.session.add(created_tag)
        db.session.commit()
        return redirect(url_for('tags_all'))


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

    tag_query = Tag.query.filter(Tag.account_id == current_user.id).all()
    tags = []
    for tag in tag_query:
        tags.append({"id": tag.id, "name": tag.name})

    return jsonify(tags)
