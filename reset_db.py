from application import db
from application.tasks.models import Category, TaskList

db.drop_all()
db.create_all()

default_category = Category(name=u'Default')
important_category = Category(name=u'Important')
extra_category = Category(name=u'Extra')
today_tasklist = TaskList(name=u'Today')
tomorrow_tasklist = TaskList(name=u'Tomorrow')
week_tasklist = TaskList(name=u'This week')

db.session.add(default_category)
db.session.add(important_category)
db.session.add(extra_category)
db.session.add(today_tasklist)
db.session.add(tomorrow_tasklist)
db.session.add(week_tasklist)
db.session.commit()
