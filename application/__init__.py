from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from application import views
from application.tasks import models
from application.tasks import views
from application.auth import models
from application.auth import views
from application.auth.models import Account

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = 'auth_login'
login_manager.login_message = 'Please login to use this functionality'

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(user_id)

try:
    db.create_all()
except:
    pass
