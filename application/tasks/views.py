from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required, current_user

from application import app, db
from application.tasks.models import Category, Task, TaskList
from application.tasks.forms import TaskForm


@app.route('/tasks/today')
@login_required
def tasks_today(form=None):
    session['url_function'] = 'tasks_today'
    result = Task.query.filter(
        (Task.tasklist_id == 1) & (Task.account_id == current_user.id) & (Task.is_completed == False)
    ).first()

    if not form:
        form = TaskForm()

    categories = Task.get_categories_by_task()
    return render_template('tasks/tasks_today.html', current_task=result, categories=categories, form=form)


@app.route('/tasks/tomorrow')
@login_required
def tasks_tomorrow(form=None):
    session['url_function'] = 'tasks_tomorrow'
    result = Task.query.filter(
        (Task.tasklist_id == 2) & (Task.account_id == current_user.id) & (Task.is_completed == False)
    ).all()
    tasks = result if result else []

    if not form:
        form = TaskForm()

    categories = Task.get_categories_by_task()
    return render_template('tasks/tasks_tomorrow.html',
                           tasks=tasks, categories=categories, form=form)


@app.route('/tasks/week')
@login_required
def tasks_week(form=None):
    session['url_function'] = 'tasks_week'
    result = Task.query.filter(
        (Task.tasklist_id == 3) & (Task.account_id == current_user.id) & (Task.is_completed == False)
    ).all()
    tasks = result if result else []

    if not form:
        form = TaskForm()

    categories = Task.get_categories_by_task()
    return render_template('tasks/tasks_week.html', tasks=tasks, categories=categories, form=form)


@app.route('/tasks/new', methods=['POST'])
@login_required
def new_task():
    if 'url_function' not in session:
        session['next'] = 'new_task'
        return redirect(url_for('auth_logout'))

    form = TaskForm(request.form)

    if not form.validate():
        return redirect(url_for(session['url_function']), form)

    form_desc = form.description.data

    list_id = -1
    if session['url_function'] == 'tasks_today':
        list_id = 1
    elif session['url_function'] == 'tasks_tomorrow':
        list_id = 2
    elif session['url_function'] == 'tasks_week':
        list_id = 3

    tasklist_result = TaskList.query.filter(TaskList.id == list_id).first()
    if tasklist_result:
        created_task = Task(current_user.id, list_id, form_desc)
        db.session.add(created_task)
        db.session.commit()
    return redirect(url_for(session['url_function']))


@app.route('/tasks/complete', methods=['POST'])
@login_required
def complete_task():
    json_data = request.json['task_id']
    task_id = int(json_data[5:]) if json_data.startswith('task_') else -1
    task = db.session.query(Task).filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()
    if task:
        task.is_completed = True
        db.session.commit()
    return url_for(session['url_function'])


@app.route('/tasks/update', methods=['POST'])
@login_required
def update_task():
    json_id_data = request.json['task_id']
    json_desc_data = request.json['desc']
    task_id = int(json_id_data[5:]) if json_id_data.startswith('task_') else -1
    task = db.session.query(Task).filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()
    if task and json_desc_data.strip():
        task.description = json_desc_data
        db.session.commit()
        return task.description
    return ""


@app.route('/tasks/update-tags', methods=['POST'])
@login_required
def update_tags():
    json_id_data = request.json['task_id']
    json_tag_data = request.json['tag_id']
    task_id = int(json_id_data[5:]) if json_id_data.startswith('task_') else -1
    tag_id = int(json_tag_data[4:]) if json_tag_data.startswith('tag-') else -1
    task = Task.query.filter(Task.id == task_id).first()
    tag = Category.query.filter(Category.id == tag_id).first()

    if task and tag:
        match = task.categories.filter(Category.id == tag.id).first()
        if match:
            task.categories.remove(tag)
            db.session.commit()
            return "removed"
        else:
            task.categories.append(tag)
            db.session.commit()
            return "added"

    return "error"


@app.route('/tasks/delete', methods=['POST'])
@login_required
def delete_task():
    json_data = request.json['task_id']
    task_id = int(json_data[5:]) if json_data.startswith('task_') else -1
    task = db.session.query(Task).filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()
    if task:
        db.session.delete(task)
        db.session.commit()
    return url_for(session['url_function'])


@app.route('/tasks/query_all_tags', methods=['POST'])
@login_required
def query_all_tags():
    tag_query = Category.query.all()
    tags = []
    for tag in tag_query:
        tags.append({"id": tag.id, "name": tag.name})

    return jsonify(tags)


@app.route('/tasks/query_tags_for_task', methods=['POST'])
@login_required
def query_tags_for_task():
    json_data = request.json['task_id']
    task_id = int(json_data[5:]) if json_data.startswith('task_') else -1
    categories = Task.get_categories_for_task(task_id)
    return jsonify(categories)
