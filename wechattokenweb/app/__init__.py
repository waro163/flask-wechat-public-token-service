from flask import Flask,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_apscheduler import APScheduler
import requests
import logging

app = Flask(__name__)
db = SQLAlchemy()
scheduler = APScheduler()
redis_store = FlaskRedis()

def gettokenjob():
    with app.app_context():
        params = {'grant_type':'client_credential',
                  'appid':current_app.config.get('APPID'),
                  'secret':current_app.config.get('APPSECRET')}
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        r = requests.get(url,params=params)
        # print r.url
        print r.json()
        redis_store.set('token_json', unicode({'access_token':r.json().get(u'access_token').encode('utf-8'),
                                               'expires_in':r.json().get(u'expires_in')}))
        redis_store.set('access_token',r.json().get('access_token'))
        redis_store.set('expires_in',r.json().get('expires_in'))


def create_app():

    from config import Config
    app.config.from_object(Config)

    db.init_app(app)
    redis_store.init_app(app)
    scheduler.init_app(app)

    gettokenjob()
    scheduler.start()
    # logging.basicConfig()
    # logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app