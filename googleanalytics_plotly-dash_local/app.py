import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np

import modules.helloanalytics as ga
import modules.hellodash as hd


def server_layout():

    viewid = '********'

    start_date = '8daysAgo'
    end_date = '1daysAgo'

    view = ga.Analytics(viewid)

    df = view.get_report(start_date
                        , end_date
                        , ['sessions', 'pageviews']
                        , ['date']
#                        , {"ga:date" : "ASCENDING"}
    )

    df_device = view.get_report(start_date
                        , end_date
                        , ['sessions']
                        , ['deviceCategory']
    )
    # dataの型変換
    df["date"] = df["date"].str[0:4] + "年" + df["date"].str[4:6] + "月" + df["date"].str[6:8] + "日"
    return html.Div(children=[
        html.H1(children='GoogleAnalytics'),
        html.Div(children='GoogleAnalytics Webデータ'),
        html.Div([hd.make_line("pv", df["date"], df["pageviews"], "line", "pv", "Weekly PV数")]),
        html.Div([
            html.Div([hd.make_pie("device", df_device["sessions"], df_device["deviceCategory"], "Weekly デバイス別セッション数")]
                , style={'width': '49%', 'display': 'inline-block'}
            ),
            html.Div([hd.make_pie("device2", df_device["sessions"], df_device["deviceCategory"], "Weekly デバイス別セッション数")]
                , style={'width': '49%', 'display': 'inline-block'}
            ),
        ]
            , style={'overflow': 'hidden'}
        )
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = server_layout

if __name__ == '__main__':
    app.run_server(debug=True)