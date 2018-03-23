from application import app, db
from application.tasks.models import Account, Category, Task, TaskList

db.drop_all()
db.create_all()

default_category = Category(name=u'Default category')
today_tasklist = TaskList(name=u'Today')
tomorrow_tasklist = TaskList(name=u'Tomorrow')
week_tasklist = TaskList(name=u'This week')

db.session.add(default_category)
db.session.add(today_tasklist)
db.session.add(tomorrow_tasklist)
db.session.add(week_tasklist)
db.session.commit()
