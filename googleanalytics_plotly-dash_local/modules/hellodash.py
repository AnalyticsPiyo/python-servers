# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

def make_line(id, x_data, values, type, name, title):
    # type は line or bar
    return dcc.Graph(
               id= id,
               figure={
                   'data': [
                       {'x': x_data, 'y': values, 'type': type, 'name': name},
                   ],
                   'layout': {
                       'title': title
                   }
               }
           )

# 円グラフ用
def make_pie(id, x_data, y_data, title):
    return dcc.Graph(
               id= id,
               figure={
                   'data': [
                       {'labels': y_data, 'values': x_data, 'type': 'pie'},
                   ],
                   'layout': {
                       'title': title
                   }
               }
           )