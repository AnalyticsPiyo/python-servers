# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from flask_bootstrap import Bootstrap

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html

import datetime
import os
import modules.MakeGantt as mg
import plotly.figure_factory as ff

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

server = Flask(__name__)
bootstrap = Bootstrap(server)
app = dash.Dash(__name__, server=server)
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

VALID_USERNAME_PASSWORD_PAIRS = [
    ['*****', '*****']
]
users = {
    "*****": "*****"
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
auth_flask = HTTPBasicAuth()

# グラフ作成のモジュール
gantt = mg.Test()

@auth_flask.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# 直観的にわかりづらいので children は削除
def serve_layout():
    
    fig_task = gantt.task()
    fig_member = gantt.member()
    
    
    return html.Div([
        html.Div([
                html.H1('**********'),
                html.Div('** ここには各ページのリンクを張る予定 **'),
                html.A('Navigate to "コンテンツTOPページ"', href='./top'),
                html.Br(),
                html.Br(),
                html.Div('*********'),
            ]
            , style={'background-color': '#eeeeee'}
        ),
        html.Div([dcc.Graph(figure=fig_task, id='gantt_task')]
        ), 
        
        html.Div(dcc.Graph(figure=fig_member, id='gantt_member')
        ),
    ])

app.layout = serve_layout

# 念のため用意
@server.route('/')
def index():
    return "Hello World"

@server.route('/top')
@auth_flask.login_required
def indexTwo():
    return render_template('index.html')

#@app.callback()
@server.route('/test')
def test():

    return ""

if __name__ == "__main__":
    server.run(host=host, port=int(port), debug=True, threaded=True)
    app.run_server(debug=True)
 