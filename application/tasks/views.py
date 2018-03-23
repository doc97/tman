from flask import render_template, redirect, url_for, request, session
from application import app, db
from application.tasks.models import Task, TaskList

@app.route('/tasks_today')
def tasks_today():
    if 'account_id' in session:
        session['url'] = '/tasks_today'
        result = Task.query.filter((Task.tasklist_id == 1) & (Task.account_id == session['account_id']) & Task.is_completed == False).first()
        return render_template('tasks_today.html', currentTask = result.description if result else "Congratulations, you have no tasks left today!")
    return redirect(url_for('logout'))

@app.route('/tasks_tomorrow')
def tasks_tomorrow():
    if 'account_id' in session:
        session['url_function'] = 'tasks_tomorrow'
        result = Task.query.filter((Task.tasklist_id == 2) & (Task.account_id == session['account_id']) & (Task.is_completed == False)).all()
        return render_template('tasks_tomorrow.html', tasks = result if result else [])
    return redirect(url_for('logout'))

@app.route('/tasks_week')
def tasks_week():
    if 'account_id' in session:
        session['url_function'] = 'tasks_week'
        result = Task.query.filter((Task.tasklist_id == 3) & (Task.account_id == session['account_id']) & (Task.is_completed == False)).all()
        return render_template('tasks_week.html', tasks = result if result else [])
    return redirect(url_for('logout'))

@app.route('/new_task', methods=['POST'])
def new_task():
    if 'account_id' in session:
        form_desc = request.form['description']

        list_id = -1
        if session['url_function'] == 'tasks_today':
            list_id = 1
        elif session['url_function'] == 'tasks_tomorrow':
            list_id = 2
        elif session['url_function'] == 'tasks_week':
            list_id = 3

        tasklist_result = TaskList.query.filter(TaskList.id == list_id).first();
        if tasklist_result:
            new_task = Task(session['account_id'], tasklist_result.id, form_desc)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for(session['url_function']))
    return redirect(url_for('logout'))

@app.route('/complete_task', methods=['POST'])
def complete_task():
    if 'account_id' in session:
        jsonData = request.json['task_id']
        task_id = int(jsonData[5:]) if jsonData.startswith('task_') else -1
        task = db.session.query(Task).filter((Task.account_id == session['account_id']) & (Task.id == task_id)).one();
        if task:
            task.is_completed = True
            db.session.commit()
        return url_for(session['url_function'])
    return url_for('logout')
