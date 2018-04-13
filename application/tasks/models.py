from application import db
from sqlalchemy.sql import text

category_task = db.Table('CategoryTask',
                         db.Column('category_id', db.Integer, db.ForeignKey('Category.id')),
                         db.Column('task_id', db.Integer, db.ForeignKey('Task.id'))
                         )


class Task(db.Model):
    __tablename__ = 'Task'
    id = db.Column('id', db.Integer, primary_key=True)
    account_id = db.Column('account_id', db.Integer, db.ForeignKey('Account.id'))
    tasklist_id = db.Column('tasklist_id', db.Integer, db.ForeignKey('TaskList.id'))
    description = db.Column('description', db.Unicode)
    is_completed = db.Column('is_completed', db.Boolean, default=False)

    account = db.relationship('Account', foreign_keys=account_id)
    tasklist = db.relationship('TaskList', foreign_keys=tasklist_id)

    def __init__(self, account_id, tasklist_id, description):
        self.account_id = account_id
        self.tasklist_id = tasklist_id
        self.description = description

    @staticmethod
    def get_categories_by_task():
        stmt = text('SELECT Task.id, Category.name FROM Category'
                    ' JOIN CategoryTask'
                    ' LEFT JOIN Task ON Task.id = CategoryTask.task_id and Category.id = CategoryTask.category_id'
                    ' GROUP BY Task.id'
                    )

        res = db.engine.execute(stmt)
        categories_by_task = {}
        for row in res:
            if not categories_by_task:
                categories_by_task[row[0]] = []
            categories_by_task[row[0]].append(row[1])

        return categories_by_task


class TaskList(db.Model):
    __tablename__ = 'TaskList'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)

    def __init__(self, name):
        self.name = name


class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)

    def __init__(self, name):
        self.name = name
