import responder
import sqlite3
import os
from datetime import datetime

datetime.now().strftime("%Y/%m/%d %H:%M:%S")
api = responder.API()

dbname = 'database.db'

@api.route("/")
async def index(req, resp):

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    # POSTされた値を格納する用の辞書変数
    tweet = None
    post_values = dict()
    cnt_rows = ""
#    print(req.params)

    # POSTされた値を格納
    if req.method == 'post':
        post_values = await req.media()

    # usernameがない かつ usernameがPOSTされていない場合、初めてのページに遷移
    if "username" not in req.session and "username" not in post_values :
        connection.close()
        resp.text = api.template('index_first.html')
        return

    # usernameがPOSTされた場合はセッションに格納、事前に持っていたらその値をusernameに使用
    if "username" in post_values:
        resp.session["username"] = post_values["username"]
        username = post_values["username"]
    else:
        username = resp.session["username"]

    # 件数取得
    cursor.execute("SELECT COUNT(*) FROM sample")
    cnt = cursor.fetchone()[0]

    # 現在時刻取得
    now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # Tweetがされた場合
    if "tweet" in post_values:
        cursor.execute("INSERT INTO sample VALUES (?, ?, ?, ?, ?)", (cnt + 1, username, now_time, post_values["tweet"], ""))
        connection.commit()

    # GETがあるかないかによってSELECT句を変更
    if req.method == 'get' and "count" in req.params:
        if int(req.params["count"]) > 10:
            cnt_rows = int(req.params["count"]) - 9
        else:
            cnt_rows = 2
        # SELECT カラム名, ... FROM テーブル名 LIMIT 行数 OFFSET 開始位置;
        cursor.execute("SELECT * FROM sample WHERE id < ? ORDER BY date DESC LIMIT ?", (cnt_rows, 10))
    else:
        cursor.execute("SELECT * FROM sample ORDER BY date DESC LIMIT 10")

    tweet = cursor.fetchall()

    connection.close()
    resp.text = api.template('index.html', tweet = tweet)

if __name__ == '__main__':
    # api.run()
    api.run(port=8080)