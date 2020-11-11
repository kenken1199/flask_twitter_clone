import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# SQLALCHEMY_DATABASE_URI = 'postgresql://kenta:kenta@localhost:5432/hogehoge'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
SECRET_KEY = 'secret key'
WTF_CSRF_ENABLED = True