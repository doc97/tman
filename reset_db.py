from application import db
from application.tasks.models import TaskList

db.drop_all()
db.create_all()

today_tasklist = TaskList(name=u'Today')
tomorrow_tasklist = TaskList(name=u'Tomorrow')
week_tasklist = TaskList(name=u'This week')

db.session.add(today_tasklist)
db.session.add(tomorrow_tasklist)
db.session.add(week_tasklist)
db.session.commit()
