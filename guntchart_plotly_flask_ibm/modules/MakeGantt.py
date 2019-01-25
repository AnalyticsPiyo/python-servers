# -*- coding: utf-8 -*-
import plotly
import plotly.plotly as py
import plotly.figure_factory as ff
import plotly.offline as offline
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class Test:
    def __init__(self):
        # jyupter notebookを使用するときに記述
        # plotly.offline.init_notebook_mode(connected=False)
        self.scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread-*******.json', self.scope)
        self.gc = gspread.authorize(self.credentials)

    def __pre(self):
        if self.credentials.access_token_expired:
            self.gc.login()  # refreshes the token
        # データの読み込み
        self.wks = self.gc.open('*************').get_worksheet(*)
        # データの取得
        df = pd.DataFrame(self.wks.get_all_values())
        # カラムの行以外を格納
        df2 = df[1:]
        # カラム名設定
        df2.columns = df[:1].values.tolist()[0]
        # データフレームのindex番号のふり直し
        df3 = df2.reset_index()
        return df3
        

    def task(self):
        task_df = self.__pre()
        # Taskカラムを生成して値を格納
        task_df['******'] = task_df['******'] + "<br>" + task_df['******'] + "<br>"+ task_df['******'] + "<br>" + task_df['******']
        # Task名で並び替え
        task_df['Start'] = pd.to_datetime(task_df['******'])
        # Task名で並び替え
        task_df = task_df.sort_values(by=["******", "******"], ascending=[False, True])
        # fig作成
        fig = ff.create_gantt(task_df
                              , index_col=''******''
                              , show_colorbar=True
                              , title = '*******'
                              , height = 1200
                              , width = 1150
                              , showgrid_x = True
                              , showgrid_y = True
        )
        # HTML生成
        offline.plot(fig, filename = './static/task.html', show_link=False, config={"displaylogo":False, "modeBarButtonsToRemove":["sendDataToCloud"]})

    def member(self):
        member_df = self.__pre()
        # Taskカラムを生成して値を格納
        member_df['*****'] = member_df['******'] + "<br>" + member_df['******']
        # 必要なカラムの抽出
        member_df2 = member_df[['******', '******', '******', '******']]
        # カラム名のリネーム
        member_df3 = member_df2.rename(columns={'******': '******', '******': '******'})
        member_df3 = member_df3.sort_values('*****')
        fig2 = ff.create_gantt(member_df3
                               , index_col='******'
                               , show_colorbar=True
                               , title = '********'
                               , height = 750
                               , width = 1150
                               , showgrid_x = True
                               , showgrid_y = True
#                               , group_tasks= True
        )
        # HTML作成
        offline.plot(fig2, filename = './static/member.html', show_link=False, config={"displaylogo":False, "modeBarButtonsToRemove":["sendDataToCloud"]})
