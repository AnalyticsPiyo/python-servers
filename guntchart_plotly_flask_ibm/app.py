# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from flask_bootstrap import Bootstrap
import os
import modules.MakeGantt as mg

# portはIBM Cloud環境から割り当てられたものを利用
if os.getenv('VCAP_APP_PORT'):
    import metrics_tracker_client
    # Trackingするなら必要
    metrics_tracker_client.track()
    host = '0.0.0.0'
    port = port = os.getenv('VCAP_APP_PORT', '8000')
else:
    # ローカル用の設定
    host = '127.0.0.1'
    port = 5000

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['DEBUG'] = True
auth = HTTPBasicAuth()
users = {
    "data-bridge": "jyutaku"
}

# グラフのモジュール呼び出し
gantt = mg.Test()

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')

@app.route('/task')
@auth.login_required
def task():
    gantt.task()
    return render_template('gantt.html',link = '/member',link_title = 'メンバースケジュール', gantt_link = './static/task.html')
 
@app.route('/member')
@auth.login_required
def member():
    gantt.member()
    return render_template('gantt.html',link = '/task',link_title = '受託スケジュール', gantt_link = './static/member.html')

if __name__ == "__main__":
    app.run(host=host, port=int(port), debug=True, threaded=True)