from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required, current_user

from application import app, db
from application.tasks.models import Tag, Task, TaskList
from application.tasks.forms import TaskForm


@app.route('/tasks/today')
@login_required
def tasks_today():
    session['url_function'] = 'tasks_today'
    not_completed_query = Task.query.filter(
        (Task.tasklist_id == 1) & (Task.account_id == current_user.id) & (Task.is_completed == False)
    ).all()
    completed_query = Task.query.filter(
        (Task.tasklist_id == 1) & (Task.account_id == current_user.id) & (Task.is_completed == True)
    ).all()

    tasks = not_completed_query if not_completed_query else []
    done_tasks = completed_query if completed_query else []
    tags = Task.get_tags_by_task()
    return render_template('tasks/tasks_today.html', tasks=tasks, done_tasks=done_tasks,
                           tags=tags, form=TaskForm())


@app.route('/tasks/tomorrow')
@login_required
def tasks_tomorrow():
    session['url_function'] = 'tasks_tomorrow'
    not_completed_query = Task.query.filter(
        (Task.tasklist_id == 2) & (Task.account_id == current_user.id) & (Task.is_completed == False)
    ).all()
    completed_query = Task.query.filter(
        (Task.tasklist_id == 2) & (Task.account_id == current_user.id) & (Task.is_completed == True)
    ).all()

    tasks = not_completed_query if not_completed_query else []
    done_tasks = completed_query if completed_query else []
    tags = Task.get_tags_by_task()
    return render_template('tasks/tasks_tomorrow.html', tasks=tasks, done_tasks=done_tasks,
                           tags=tags, form=TaskForm())


@app.route('/tasks/week')
@login_required
def tasks_week():
    session['url_function'] = 'tasks_week'
    not_completed_query = Task.query.filter(
        (Task.tasklist_id == 3) & (Task.account_id == current_user.id) & (Task.is_completed == False)
    ).all()
    completed_query = Task.query.filter(
        (Task.tasklist_id == 3) & (Task.account_id == current_user.id) & (Task.is_completed == True)
    ).all()

    tasks = not_completed_query if not_completed_query else []
    done_tasks = completed_query if completed_query else []
    tags = Task.get_tags_by_task()
    return render_template('tasks/tasks_week.html', tasks=tasks, done_tasks=done_tasks,
                           tags=tags, form=TaskForm())


@app.route('/tasks/new', methods=['POST'])
@login_required
def new_task():
    if 'url_function' not in session:
        session['next'] = 'new_task'
        return redirect(url_for('auth_logout'))

    form = TaskForm(request.form)

    if not form.validate():
        return redirect(url_for(session['url_function']))

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
    task_id = int(json_data[5:]) if json_data.startswith('task-') else -1
    task = Task.query.filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()
    if task:
        task.is_completed = True
        db.session.commit()
    return url_for(session['url_function'])


@app.route('/tasks/undo', methods=['POST'])
@login_required
def undo_completed_task():
    json_data = request.json['task_id']
    task_id = int(json_data[5:]) if json_data.startswith('task-') else -1
    task = Task.query.filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()
    if task:
        task.is_completed = False
        db.session.commit()
    return url_for(session['url_function'])


@app.route('/tasks/update', methods=['POST'])
@login_required
def update_task():
    json_id_data = request.json['task_id']
    json_desc_data = request.json['desc']
    task_id = int(json_id_data[5:]) if json_id_data.startswith('task-') else -1
    task = Task.query.filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()
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
    task_id = int(json_id_data[5:]) if json_id_data.startswith('task-') else -1
    tag_id = int(json_tag_data[4:]) if json_tag_data.startswith('tag-') else -1
    task = Task.query.filter(Task.id == task_id).first()
    tag = Tag.query.filter(Tag.id == tag_id).first()

    if task and tag:
        match = task.tags.filter(Tag.id == tag.id).first()
        if match:
            task.tags.remove(tag)
            db.session.commit()
            return "removed"
        else:
            task.tags.append(tag)
            db.session.commit()
            return "added"

    return "error"


@app.route('/tasks/move', methods=['POST'])
@login_required
def move_task():
    json_id_data = request.json['task_id']
    json_list_data = request.json['list_id']
    task_id = int(json_id_data[5:]) if json_id_data.startswith('task-') else -1
    list_id = int(json_list_data[5:]) if json_list_data.startswith('move-') else -1
    task = Task.query.filter(Task.id == task_id).first()
    tasklist = TaskList.query.filter(TaskList.id == list_id).first()

    if task and tasklist:
        task.tasklist_id = tasklist.id
        db.session.commit()

    return url_for(session['url_function'])


@app.route('/tasks/delete', methods=['POST'])
@login_required
def delete_task():
    json_data = request.json['task_id']
    task_id = int(json_data[5:]) if json_data.startswith('task-') else -1
    task = Task.query.filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()
    if task:
        db.session.delete(task)
        db.session.commit()
    return url_for(session['url_function'])


@app.route('/tasks/query_all_tags', methods=['POST'])
@login_required
def query_all_tags():
    tag_query = Tag.query.all()
    tags = []
    for tag in tag_query:
        tags.append({"id": tag.id, "name": tag.name})

    return jsonify(tags)


@app.route('/tasks/query_tags_for_task', methods=['POST'])
@login_required
def query_tags_for_task():
    json_data = request.json['task_id']
    task_id = int(json_data[5:]) if json_data.startswith('task-') else -1
    tags = Task.get_tags_for_task(task_id)
    return jsonify(tags)
