import os

DEBUG = True
SECRET_KEY = os.urandom(32)
USE_SESSION_FOR_NEXT = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

if os.environ.get('HEROKU'):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    SQLALCHEMY_ECHO = True
