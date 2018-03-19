import os

DEBUG = True
SECRET_KEY = b'Em\x9b\xf6\xd5\xd3\xac\xad2\x88\xe1\xf4p\x11L8\xbf\x8c0\xe0_2\xb2\x86'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
