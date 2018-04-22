from application import db
from application.tasks.models import Tag, TaskList

db.drop_all()
db.create_all()

default_tag = Tag(name=u'Default')
important_tag = Tag(name=u'Important')
extra_tag = Tag(name=u'Extra')
today_tasklist = TaskList(name=u'Today')
tomorrow_tasklist = TaskList(name=u'Tomorrow')
week_tasklist = TaskList(name=u'This week')

db.session.add(default_tag)
db.session.add(important_tag)
db.session.add(extra_tag)
db.session.add(today_tasklist)
db.session.add(tomorrow_tasklist)
db.session.add(week_tasklist)
db.session.commit()
