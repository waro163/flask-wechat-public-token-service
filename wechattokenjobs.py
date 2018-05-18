# -*- coding: utf-8 -*-
from flask import Flask,current_app
from flask_apscheduler import APScheduler
import json
import requests
import logging
from flask_redis import FlaskRedis

app = Flask(__name__)
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

class Config(object):
    JOBS = [
        {
            'id': 'gettokenjob',
            # 'func': 'wechattokenjobs:gettokenjob',
            'func': gettokenjob,
            'args': None,
            'trigger': 'interval',
            'seconds': 3600,
        }
    ]

    SCHEDULER_API_ENABLED = True
    REDIS_URL = "redis://:XXXXXXXX@localhost:6379/0"
    APPID = 'XXXXXXXXXXX'
    APPSECRET = 'XXXXXXXXXXXXXX'

@app.route('/addjob')
def addtask():
    scheduler.add_job(func=gettokenjob,id='test',args=None,trigger='interval',seconds=5)
    return 'add task success'

@app.route('/pause/<id>')
def pausetask(id=None):
    if id:
        scheduler.pause_job(id)
        return '%s had beed pause' % id
    else:
        return 'seem you forget task id '

@app.route('/resume/<id>')
def resumetask(id):
    scheduler.resume_job(id)
    return '%s had beed resume' % id


@app.route('/remove/<id>')
def removetask(id):
    scheduler.remove_job(id)
    return '%s had beed removed' % id

@app.route('/getjobs')
def getjobs():
    jobs = {}
    print scheduler.get_jobs()
    for k in scheduler.get_jobs():
        print k.id, k.name
        jobs.update({k.id:k.name})
    return json.dumps(jobs)

@app.route('/updatetoken')
def dojob():
    gettokenjob()
    return 'job had done once'

@app.route('/gettoken')
def gettoken():
    # token_json = {'access_token':redis_store.get('access_token'),'expires_in':redis_store.get('expires_in')}
    # return json.dumps(token_json)

    return json.dumps(redis_store.get('token_json'))

if __name__ == '__main__':

    app.config.from_object(Config())

    redis_store.init_app(app)
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    #in order to execute the task instantly
    gettokenjob()
    scheduler.start()
    #
    # logging.basicConfig()
    # logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    app.run()
