# -*- coding: utf-8 -*-
import json
from . import main
from flask import render_template,request,current_app,redirect,url_for
from .. import redis_store,gettokenjob,scheduler

@main.route('/',methods=['GET','POST'])
def index():
    # print request.args
    # print json.dumps(request.args)
    return 'Hello world'

@main.route('/addjob')
def addtask():
    scheduler.add_job(func=gettokenjob,id='test',args=None,trigger='interval',seconds=5)
    return 'add task success'

@main.route('/pause/<id>')
def pausetask(id=None):
    if id:
        scheduler.pause_job(id)
        return '%s had beed pause' % id
    else:
        return 'seem you forget task id '

@main.route('/resume/<id>')
def resumetask(id):
    scheduler.resume_job(id)
    return '%s had beed resume' % id


@main.route('/remove/<id>')
def removetask(id):
    scheduler.remove_job(id)
    return '%s had beed removed' % id

@main.route('/getjobs')
def getjobs():
    jobs = {}
    print scheduler.get_jobs()
    for k in scheduler.get_jobs():
        print k.id, k.name
        jobs.update({k.id:k.name})
    return json.dumps(jobs)

@main.route('/updatetoken')
def dojob():
    gettokenjob()
    return redirect(url_for('main.gettoken'))

@main.route('/gettoken')
def gettoken():
    # token_json = {'access_token':redis_store.get('access_token'),'expires_in':redis_store.get('expires_in')}
    # return json.dumps(token_json)

    return json.dumps(redis_store.get('token_json'))