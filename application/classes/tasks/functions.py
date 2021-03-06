from flask_login import current_user

from application import db
from application.classes.tasks.models import Task

import application.session_state as state


def url_function_to_int():
    if state.query('url_function') == 'tasks_today':
        return 1
    elif state.query('url_function') == 'tasks_tomorrow':
        return 2
    elif state.query('url_function') == 'tasks_week':
        return 3
    return -1


def update_ordering_count():
    if state.equals('url_function', 'tasks_today'):
        state.inc('today_ordering_count')
    elif state.equals('url_function', 'tasks_tomorrow'):
        state.inc('tomorrow_ordering_count')
    elif state.equals('url_function', 'tasks_week'):
        state.inc('week_ordering_count')


def normalize_ordering():
    if state.query('today_ordering_count') >= 10:
        state.save('today_ordering_count', 0)
        normalize_tasklist_ordering(1)
    if state.query('tomorrow_ordering_count') >= 10:
        state.save('tomorrow_ordering_count', 0)
        normalize_tasklist_ordering(2)
    if state.query('week_ordering_count') >= 10:
        state.save('week_ordering_count', 0)
        normalize_tasklist_ordering(3)


def normalize_tasklist_ordering(tasklist_id):
    today_tasks = Task.query.filter(
        (Task.tasklist_id == tasklist_id) & (Task.account_id == current_user.id) & (Task.is_completed == False)
    ).order_by(Task.order).all()
    for i in range(len(today_tasks)):
        today_tasks[i].order = i + 1

    db.session.commit()
