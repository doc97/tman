from tman import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

category_task = db.Table('category_task',
        db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
        db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
)

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column('id', db.Integer, primary_key=True)
    account_id = db.Column('account_id', db.Integer, db.ForeignKey('account.id'))
    tasklist_id = db.Column('tasklist_id', db.Integer, db.ForeignKey('tasklist.id'))
    description = db.Column('description', db.Unicode)
    is_completed = db.Column('is_completed', db.Boolean, default=False)

    account = db.relationship('Account', foreign_keys=account_id)
    tasklist = db.relationship('TaskList', foreign_keys=tasklist_id)

    def __init__(self, tasklist_id, description):
        self.tasklist_id = tasklist_id
        self.description = description

class TaskList(db.Model):
    __tablename__ = 'tasklist'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)

    def __init__(self, name):
        self.name = name

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.Unicode)
    password = db.Column('password', db.Unicode)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)

    def __init__(self, name):
        self.name = name
