from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from application import views
from application.tasks import models
from application.tasks import views

db.create_all()
