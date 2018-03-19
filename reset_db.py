from tman import app
from db_model import Account, Category, Task, TaskList, db

db.drop_all()
db.create_all()

default_category = Category(name=u'default category')
today_tasklist = TaskList(name=u'Today')
tomorrow_tasklist = TaskList(name=u'Tomorrow')
week_tasklist = TaskList(name=u'This week')

db.session.add(default_category)
db.session.add(today_tasklist)
db.session.add(tomorrow_tasklist)
db.session.add(week_tasklist)
db.session.commit()
