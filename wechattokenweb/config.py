import os
from app import gettokenjob
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    JOBS = [
        {
            'id': 'gettokenjob',
            'func': gettokenjob,
            'args': None,
            'trigger': 'interval',
            'seconds': 3600,
        }
    ]

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SCHEDULER_API_ENABLED = True
    REDIS_URL = "redis://:XXXXX@localhost:6379/0"
    APPID = 'XXXXXXX'
    APPSECRET = 'XXXXXXX'
