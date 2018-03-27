from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user

from application import app, db
from application.tasks.models import Task, TaskList
from application.tasks.forms import TaskForm

@app.route('/tasks_today')
@login_required
def tasks_today(form = None):
    session['url_function'] = 'tasks_today'
    result = Task.query.filter((Task.tasklist_id == 1) & (Task.account_id == current_user.id) & (Task.is_completed == False)).first()
    currentTask = result.description if result else "Congratulations, you have no tasks left today!"
    if not form:
        form = TaskForm()
    return render_template('tasks/tasks_today.html', currentTask = currentTask, form = form)

@app.route('/tasks_tomorrow')
@login_required
def tasks_tomorrow(form = None):
    session['url_function'] = 'tasks_tomorrow'
    result = Task.query.filter((Task.tasklist_id == 2) & (Task.account_id == current_user.id) & (Task.is_completed == False)).all()
    tasks = result if result else []
    if not form:
        form = TaskForm()
    return render_template('tasks/tasks_tomorrow.html', tasks = tasks, form = form)

@app.route('/tasks_week')
@login_required
def tasks_week(form = None):
    session['url_function'] = 'tasks_week'
    result = Task.query.filter((Task.tasklist_id == 3) & (Task.account_id == current_user.id) & (Task.is_completed == False)).all()
    tasks = result if result else []
    if not form:
        form = TaskForm()
    return render_template('tasks/tasks_week.html', tasks = tasks, form = form)

@app.route('/new_task', methods=['POST'])
@login_required
def new_task():
    if 'url_function' in session:
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


        tasklist_result = TaskList.query.filter(TaskList.id == list_id).first();
        if tasklist_result:
            new_task = Task(current_user.id, list_id, form_desc)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for(session['url_function']))
    return redirect(url_for('auth_logout'))

@app.route('/complete_task', methods=['POST'])
@login_required
def complete_task():
    jsonData = request.json['task_id']
    task_id = int(jsonData[5:]) if jsonData.startswith('task_') else -1
    task = db.session.query(Task).filter((Task.account_id == current_user.id) & (Task.id == task_id)).one();
    if task:
        task.is_completed = True
        db.session.commit()
    return url_for(session['url_function'])
