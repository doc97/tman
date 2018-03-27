import os

DEBUG = True
SECRET_KEY = os.urandom(32)
SQLALCHEMY_TRACK_MODIFICATIONS = False

if os.environ.get('HEROKU'):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
else:
    SQLALCHEMY_DATABASE_URI = "postgresql:///testdb"
    SQLALCHEMY_ECHO = True
