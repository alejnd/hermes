#!/usr/bin/env python
#  coding: utf-8
import hermes
from ConfigParser import SafeConfigParser
from flask import Flask, jsonify, request, abort, url_for, render_template, g, flash, redirect
from functools import wraps
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
import time
from logmanager import log
from flask import json
from dbmanager import Database
import user
#TODO: each service has differents url to support multiple accounts 

config = SafeConfigParser()
config.read('hermes.cfg')
notifyAgent = hermes.Hermes(config)


server_ipaddr    = config.get('server','addr')
server_port      = config.get('server','port')
server_whitelist = config.get('server','whitelist')
server_debug     = config.get('server','debug')

#--- valid parameters ---
twitter_required_parameters = set(['msg','log_level'])
mail_required_parameters   = set(['msg','log_level','to','subject'])

#--- init dbmanager ---
db =Database()
app = Flask(__name__)

#--- Loggining ---
app.secret_key = '\x16\x91\xa4ZPL\xe6=%\xb6\x94\xe3<Cg\x1e\x00f21\x92\x8aq\x15'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
user = user.User(config)

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(id):
    if user.id == id: return user
    return None

def check_whitelist(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        log.debug(request.get_json())
        if request.remote_addr not in server_whitelist: return 'forbidden',401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/twitter/notify', methods = ['POST'])
@check_whitelist
def twitter_notify():
    if not request.json: abort(400)
    if set((request.get_json().keys())) != twitter_required_parameters: return jsonify({'result': False})
    
    timestamp = time.strftime('%Y-%M-%d %H:%M:%S',time.localtime())
    loglevel  = str(request.json['log_level']).upper()
    msg       = loglevel+': '+str(request.json['msg'])
    
    db.insertMessage(timestamp, loglevel, 'twitter', msg)
    try: notifyAgent.twitterrobot.Sendmsg(msg)
    except: return jsonify({'result': False})
    db.setDelivered()
    return jsonify({'result': True})
    
@app.route('/mail/notify', methods = ['POST'])
@check_whitelist
def mail_notify():
    if not request.json: abort(400)
    if set((request.get_json().keys())) != mail_required_parameters: return jsonify({'result': False})
    
    timestamp = time.strftime('%Y-%M-%d %H:%M:%S',time.localtime())
    to        = str(request.json['to'])
    subject   = str(request.json['subject'])
    loglevel  = str(request.json['log_level']).upper()
    msg       = loglevel+': '+str(request.json['msg'])
    db.insertMessage(timestamp, loglevel, 'mail', msg, subject)
    try: notifyAgent.mailrobot.Sendmsg(to,msg,subject)
    except: return jsonify({'result': False})
    db.setDelivered()
    return jsonify({'result': True})


@app.route('/')
@app.route('/index.html')
@login_required
def index():
    print str(request.remote_addr)
    last_messages = db.get_last_messages(10)
    return render_template('index.html', result=last_messages)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    if  user.username == username and user.password == password: 
        login_user(user)
        flash('Logged in successfully')
        return redirect(url_for('index'))
    else:
        flash('Username or Password is invalid' , 'error')
        logout_user()
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
        
if __name__ == '__main__':
    app.run(host=server_ipaddr, port=int(server_port), debug=server_debug)

