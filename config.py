import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfiguration(object):
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'nine east crab anything rather dissuade'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'toboggan.sqlite3')
    DEBUG = True

class TestConfiguration(BaseConfiguration):
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
