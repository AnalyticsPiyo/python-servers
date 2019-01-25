# -*- coding: utf-8 -*-
import plotly
import plotly.plotly as py
import plotly.figure_factory as ff
import plotly.offline as offline
import gspread
import pandas as pd
import datetime
from oauth2client.service_account import ServiceAccountCredentials

class Test:
    def __init__(self):
        # jyupter notebookを使用するときに記述
        # plotly.offline.init_notebook_mode(connected=False)
        self.scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread-********.json', self.scope)
        self.gc = gspread.authorize(self.credentials)

    def __pre(self):
        if self.credentials.access_token_expired:
            self.gc.login()  # refreshes the token
        # データの読み込み
        self.wks = self.gc.open('********').get_worksheet(5)
        # データの取得
        df = pd.DataFrame(self.wks.get_all_values())
        # カラムの行以外を格納
        df2 = df[1:]
        # カラム名設定
        df2.columns = df[:1].values.tolist()[0]
        
        # 日付型に変更
        df2['****'] = pd.to_datetime(df2['****'])
        df2['****'] = pd.to_datetime(df2['****'])
        
        ### 必要であれば日付(finish)でフィルタをかける ###
        df2 = df2[df2.Finish >= datetime.date.today()]
        return df2
        

    def task(self):
        task_df = self.__pre()
        # Taskカラムを生成して値を格納
        task_df['Task'] = task_df['Client'] + "<br>" + task_df['PRJ'] + "<br>"+ task_df['Catergory'] + "<br>" + task_df['Subcatergory']

        # Task名で並び替え
        task_df = task_df.sort_values(by=["Client", "PRJ", "Start"], ascending=[True, True, True])
        task_df = task_df.reset_index(drop=True)
        # fig作成
        fig = ff.create_gantt(task_df
                              , index_col='Resource'
                              , show_colorbar=True
                              , title = '<****>'
                              , height = 1200
                              , width = 1200
#                              , marginLeft="auto"
#                              , marginRight="auto"
#                              , marginBottom="10px"
                              , showgrid_x = True
                              , showgrid_y = True
        )
        # HTML生成
        return fig

    def member(self):
        member_df = self.__pre()
        # Taskカラムを生成して値を格納
        member_df['Tmp'] = member_df['Client'] + "<br>" + member_df['PRJ']
        # 必要なカラムの抽出
        member_df2 = member_df[["Resource", "Start", "Finish", "Tmp"]]
        # カラム名のリネーム
        member_df3 = member_df2.rename(columns={'Resource': 'Task', 'Tmp': 'Resource'})
        member_df3 = member_df3.sort_values('Task')
        member_df3 = member_df3.reset_index(drop=True)
        
        fig2 = ff.create_gantt(member_df3
                              , index_col='Resource'
                              , show_colorbar=True
                              , title = '<****>'
                              , height = 750
                              , width = 1200
#                              , marginLeft="auto"
#                              , marginRight="auto"
                              , showgrid_x = True
                              , showgrid_y = True
#                              , group_tasks= True
        )
        # HTML作成
        return fig2
