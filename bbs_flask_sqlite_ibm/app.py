# memo
# del flask.session['名前']

import flask
import sqlite3
from datetime import datetime

# sqlite の設定 
db = sqlite3.connect("database.db")
conn = db.cursor()
conn.execute("""
        SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='tbl'
        """)
if conn.fetchone()[0] == 0:
    conn.execute('CREATE TABLE tbl (name, text, time)')
conn.close()
"""
result = db.execute('SELECT * FROM tbl')
data = result.fetchall()
print(data)
"""

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '*********'

@app.route('/')
def index():
    # ログインフォーム作成
    return '''
    <h1>*********</h1>
    *********
    <br>
    <br>
    <form action="/board">
        ユーザー名: <input name="name"><br>
        <input type="submit" value="ログイン"><br>
    </form>
    '''
@app.route('/board')
def board():
    # 初回訪問かリピーターで挙動を変える

    if flask.request.args.get('name') is not None:
        flask.session['name'] = flask.request.args.get('name')

    if 'name' in flask.session:
        db = sqlite3.connect("database.db")
        conn = db.cursor()
        if flask.request.args.get('text') is not None:
            hitTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            conn.execute('INSERT INTO tbl VALUES (?, ?, ?)', (flask.session['name'], flask.request.args.get('text'), hitTime))
            db.commit()

        result = conn.execute('SELECT * FROM tbl ORDER BY time DESC ')
        data = result.fetchall()
        conn.close()
        result = ""
        for i in data:
            result = result + i[0] + " " + i[2].split(" ")[1] +  '<br>'
            result = result + "　" + i[1] + '<br>'

        response =  '<h1>*********</h1>'  \
            + '<form action="/board">'  \
            + '<input name="text"><br>' \
            + '<input type="submit" value="投稿する"><br>' \
            + '</form>' \
            + result 

        return  response
    else:
        return 'まずはニックネームを入力してください<br><br><a href="/">トップページ</a>'
   
@app.route('/mypage')
def mypage():
    return flask.session['name'] + 'さんのページ'

@app.route('/receive')
def receive():
    return '入力されたデータは"' + flask.request.args.get('value') + '"です'

if __name__ == '__main__':
    app.run()
