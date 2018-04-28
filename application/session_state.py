from flask import url_for, session


def save(key, value):
    session[key] = value


def inc(key):
    session[key] += 1


def query(key):
    return session[key] if key in session else None


def equals(key, value):
    return key in session and session[key] == value


def initialize():
    session['url_function'] = 'tasks_today'
    session['today_ordering_count'] = 0
    session['tomorrow_ordering_count'] = 0
    session['week_ordering_count'] = 0


def validate():
    if 'url_function' not in session:
        return False
    elif 'today_ordering_count' not in session:
        return False
    elif 'tomorrow_ordering_count' not in session:
        return False
    elif 'week_ordering_count' not in session:
        return False
    return True


def url_function_to_int():
    if session['url_function'] == 'tasks_today':
        return 1
    elif session['url_function'] == 'tasks_tomorrow':
        return 2
    elif session['url_function'] == 'tasks_week':
        return 3
    return -1


def get_url_for_function():
    return url_for(session['url_function'])



