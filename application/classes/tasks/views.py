from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc

from application import app, db
from application.classes.tags.models import Tag
from application.classes.tasks.models import Task, TaskList
from application.classes.tasks.forms import TaskForm

import application.session_state as state
import application.classes.tasks.functions as func


@app.route('/tasks/today')
@login_required
def tasks_today():
    state.save('url_function', 'tasks_today')
    not_completed_query = Task.query.filter(
        (Task.tasklist_id == 1) & (Task.account_id == current_user.id) & (Task.is_completed == False)
    ).order_by(Task.order).all()
    completed_query = Task.query.filter(
        (Task.tasklist_id == 1) & (Task.account_id == current_user.id) & (Task.is_completed == True)
    ).order_by(Task.order).all()

    tasks = not_completed_query if not_completed_query else []
    done_tasks = completed_query if completed_query else []
    tags = Task.get_tags_by_task()
    return render_template('tasks/tasks_today.html', tasks=tasks, done_tasks=done_tasks,
                           tags=tags, form=TaskForm())


@app.route('/tasks/tomorrow')
@login_required
def tasks_tomorrow():
    state.save('url_function', 'tasks_tomorrow')
    not_completed_query = Task.query.filter(
        (Task.tasklist_id == 2) & (Task.account_id == current_user.id) & (Task.is_completed == False)
    ).order_by(Task.order).all()
    completed_query = Task.query.filter(
        (Task.tasklist_id == 2) & (Task.account_id == current_user.id) & (Task.is_completed == True)
    ).order_by(Task.order).all()

    tasks = not_completed_query if not_completed_query else []
    done_tasks = completed_query if completed_query else []
    tags = Task.get_tags_by_task()
    return render_template('tasks/tasks_tomorrow.html', tasks=tasks, done_tasks=done_tasks,
                           tags=tags, form=TaskForm())


@app.route('/tasks/week')
@login_required
def tasks_week():
    state.save('url_function', 'tasks_week')
    not_completed_query = Task.query.filter(
        (Task.tasklist_id == 3) & (Task.account_id == current_user.id) & (Task.is_completed == False)
    ).order_by(Task.order).all()
    completed_query = Task.query.filter(
        (Task.tasklist_id == 3) & (Task.account_id == current_user.id) & (Task.is_completed == True)
    ).order_by(Task.order).all()

    tasks = not_completed_query if not_completed_query else []
    done_tasks = completed_query if completed_query else []
    tags = Task.get_tags_by_task()
    return render_template('tasks/tasks_week.html', tasks=tasks, done_tasks=done_tasks,
                           tags=tags, form=TaskForm())


@app.route('/tasks/search')
@login_required
def tasks_search():
    if not state.validate():
        state.save('next', 'tasks_search')
        return redirect(url_for('auth_logout'))
    state.save('url_function', 'tasks_search')

    search_param = "%" + request.args.get("q", default="", type=str) + "%"

    today_query = Task.query.outerjoin(Task.tags).filter(
        (Task.account_id == current_user.id) & (Task.tasklist_id == 1) &
        (Task.description.like(search_param) | (Tag.name.like(search_param)))
    ).all()
    tomorrow_query = Task.query.outerjoin(Task.tags).filter(
        (Task.account_id == current_user.id) & (Task.tasklist_id == 2) &
        (Task.description.like(search_param) | (Tag.name.like(search_param)))
    ).all()
    week_query = Task.query.outerjoin(Task.tags).filter(
        (Task.account_id == current_user.id) & (Task.tasklist_id == 3) &
        (Task.description.like(search_param) | (Tag.name.like(search_param)))
    ).all()
    today_tasks = today_query if today_query else []
    tomorrow_tasks = tomorrow_query if tomorrow_query else []
    week_tasks = week_query if week_query else []
    tags = Task.get_tags_by_task()

    return render_template('tasks/tasks_search.html', today_tasks=today_tasks, tomorrow_tasks=tomorrow_tasks,
                           week_tasks=week_tasks, tags=tags, form=TaskForm())


@app.route('/tasks/new', methods=['POST'])
@login_required
def new_task():
    if not state.validate():
        state.save('next', 'tasks_today')
        return redirect(url_for('auth_logout'))

    form = TaskForm(request.form)

    if not form.validate():
        return redirect(state.get_url_for_function())

    form_desc = form.description.data

    list_id = func.url_function_to_int()
    tasklist_result = TaskList.query.filter(TaskList.id == list_id).first()
    if tasklist_result:
        last_task = Task.query.filter(
            (Task.tasklist_id == list_id) & (Task.account_id == current_user.id) & (Task.is_completed == False)
        ).order_by(desc(Task.order)).first()
        order = last_task.order + 1 if last_task else 1
        created_task = Task(current_user.id, list_id, order, form_desc)
        db.session.add(created_task)
        db.session.commit()
    return redirect(state.get_url_for_function())


@app.route('/tasks/complete', methods=['POST'])
@login_required
def complete_task():
    if not state.validate():
        state.save('next', 'tasks_today')
        return redirect(url_for('auth_logout'))

    json_data = request.json['task_id']
    task_id = int(json_data[5:]) if json_data.startswith('task-') else -1
    task = Task.query.filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()
    if task:
        list_id = func.url_function_to_int()
        task_count = Task.query.filter(
            (Task.tasklist_id == list_id) & (Task.account_id == current_user.id) & (Task.is_completed == True)
        ).count()
        task.is_completed = True
        task.order = task_count + 1
        db.session.commit()
    return state.get_url_for_function()


@app.route('/tasks/undo', methods=['POST'])
@login_required
def undo_completed_task():
    if not state.validate():
        state.save('next', 'tasks_today')
        return redirect(url_for('auth_logout'))

    json_data = request.json['task_id']
    task_id = int(json_data[5:]) if json_data.startswith('task-') else -1
    task = Task.query.filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()
    if task:
        list_id = func.url_function_to_int()
        last_task = Task.query.filter(
            (Task.tasklist_id == list_id) & (Task.account_id == current_user.id) & (Task.is_completed == False)
        ).order_by(desc(Task.order)).first()
        task.is_completed = False
        task.order = last_task.order + 1 if last_task else 1
        db.session.commit()
    return state.get_url_for_function()


@app.route('/tasks/update', methods=['POST'])
@login_required
def update_task():
    if not state.validate():
        state.save('next', 'tasks_today')
        return redirect(url_for('auth_logout'))

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
    if not state.validate():
        state.save('next', 'tasks_today')
        return redirect(url_for('auth_logout'))

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
            return tag.name

    return "error"


@app.route('/tasks/move', methods=['POST'])
@login_required
def move_task():
    if not state.validate():
        state.save('next', 'tasks_today')
        return redirect(url_for('auth_logout'))

    json_id_data = request.json['task_id']
    json_list_data = request.json['list_id']
    task_id = int(json_id_data[5:]) if json_id_data.startswith('task-') else -1
    list_id = int(json_list_data[5:]) if json_list_data.startswith('move-') else -1
    task = Task.query.filter(Task.id == task_id).first()
    tasklist = TaskList.query.filter(TaskList.id == list_id).first()

    if task and tasklist:
        task.tasklist_id = tasklist.id
        db.session.commit()

    return state.get_url_for_function()


@app.route('/tasks/delete', methods=['POST'])
@login_required
def delete_task():
    if not state.validate():
        state.save('next', 'tasks_today')
        return redirect(url_for('auth_logout'))

    json_data = request.json['task_id']
    task_id = int(json_data[5:]) if json_data.startswith('task-') else -1
    task = Task.query.filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()
    if task:
        db.session.delete(task)
        db.session.commit()
    return state.get_url_for_function()


@app.route('/tasks/query_tags_for_task', methods=['POST'])
@login_required
def query_tags_for_task():
    if not state.validate():
        state.save('next', 'query_tags_for_task')
        return redirect(url_for('auth_logout'))

    json_data = request.json['task_id']
    task_id = int(json_data[5:]) if json_data.startswith('task-') else -1
    tags = Task.get_tags_for_task(task_id)
    return jsonify(tags)


@app.route('/tasks/order_task', methods=['POST'])
@login_required
def order_task():
    if not state.validate():
        state.save('next', 'order_task')
        return redirect(url_for('auth_logout'))

    json_id_data = request.json['task_id'] if 'task_id' in request.json else ''
    json_offset_data = request.json['offset'] if 'offset' in request.json else -1
    task_id = int(json_id_data[5:]) if json_id_data.startswith('task-') else -1
    offset = int(json_offset_data)
    offset_amount = abs(offset) + 1

    task = Task.query.filter((Task.account_id == current_user.id) & (Task.id == task_id)).first()

    if offset < 0:
        surrounding_tasks = Task.query.filter((Task.account_id == current_user.id) &
                                              (Task.tasklist_id == task.tasklist_id) &
                                              (Task.order < task.order)
                                              ).order_by(Task.order.desc()).limit(offset_amount).all()
    else:
        surrounding_tasks = Task.query.filter((Task.account_id == current_user.id) &
                                              (Task.tasklist_id == task.tasklist_id) &
                                              (Task.order > task.order)
                                              ).order_by(Task.order.asc()).limit(offset_amount).all()

    if task and surrounding_tasks:
        if len(surrounding_tasks) == offset_amount:
            prev_task_order = surrounding_tasks[0].order
            next_task_order = surrounding_tasks[1].order
        elif offset < 0:
            prev_task_order = 0
            next_task_order = surrounding_tasks[0].order
        elif offset > 0:
            prev_task_order = surrounding_tasks[0].order
            next_task_order = prev_task_order + 2
        else:
            return ""

        new_task_order = (prev_task_order + next_task_order) / 2
        task.order = new_task_order
        db.session.commit()

        func.update_ordering_count()
        func.normalize_ordering()

    return ""
