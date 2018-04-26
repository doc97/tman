from application import db
from sqlalchemy.sql import text

task_tag = db.Table('TaskTag',
                    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id')),
                    db.Column('task_id', db.Integer, db.ForeignKey('Task.id'))
                    )


class Task(db.Model):
    __tablename__ = 'Task'
    id = db.Column('id', db.Integer, primary_key=True)
    account_id = db.Column('account_id', db.Integer, db.ForeignKey('Account.id'), nullable=False)
    tasklist_id = db.Column('tasklist_id', db.Integer, db.ForeignKey('TaskList.id'), nullable=False)

    order = db.Column('order', db.Numeric(precision=16), nullable=False)
    description = db.Column('description', db.Unicode, nullable=False)
    is_completed = db.Column('is_completed', db.Boolean, default=False)

    tags = db.relationship("Tag", secondary=task_tag, collection_class=set,
                                 lazy="dynamic", backref="tasks")
    account = db.relationship('Account', foreign_keys=account_id)
    tasklist = db.relationship('TaskList', foreign_keys=tasklist_id)

    def __init__(self, account_id, tasklist_id, order, description):
        self.account_id = account_id
        self.tasklist_id = tasklist_id
        self.order = order
        self.description = description

    @staticmethod
    def get_tags_by_task():
        stmt_string = ('SELECT \"Task\".id, \"Tag\".id, \"Tag\".name FROM \"Tag\"'
                       ' CROSS JOIN \"TaskTag\"'
                       ' INNER JOIN \"Task\" ON \"Task\".id = \"TaskTag\".task_id and'
                       '\"Tag\".id = \"TaskTag\".tag_id')

        res = db.engine.execute(stmt_string)
        tags_by_task = {}
        for row in res:
            if row[0]:
                if row[0] not in tags_by_task:
                    tags_by_task[row[0]] = []
                tags_by_task[row[0]].append({"id": row[1], "name": row[2]})

        return tags_by_task

    @staticmethod
    def get_tags_for_task(task_id):
        stmt_string = ('SELECT \"Tag\".id, \"Tag\".name FROM \"Tag\"'
                       ' INNER JOIN \"TaskTag\" ON \"TaskTag\".task_id = ' + str(task_id) +
                       ' and \"TaskTag\".tag_id = \"Tag\".id')

        res = db.engine.execute(text(stmt_string))
        tags = []
        for row in res:
            tags.append({"id": row[0], "name": row[1]})
        return tags


class TaskList(db.Model):
    __tablename__ = 'TaskList'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode, nullable=False)

    def __init__(self, name):
        self.name = name


class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode, nullable=False)

    def __init__(self, name):
        self.name = name
