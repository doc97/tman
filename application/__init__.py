from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from application import views
from application.classes.tasks import models
from application.classes.tasks import views
from application.classes.tags import views
from application.classes.auth import models
from application.classes.auth import views
from application.classes.auth.models import Account

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_login'
login_manager.login_message = 'Please log in to use this functionality'


@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(user_id)


try:
    db.create_all()
except:
    pass
