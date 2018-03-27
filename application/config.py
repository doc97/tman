import os

DEBUG = True
SECRET_KEY = os.urandom(32)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Session
SESSION_TYPE = 'sqlalchemy'
SESSION_PERMANENT = False
PERMANENT_SESSION_LIFETIME = 3600 # seconds

if os.environ.get('HEROKU'):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
else:
    SQLALCHEMY_DATABASE_URI = "sqlite:///tasks.db"
    SQLALCHEMY_ECHO = True
