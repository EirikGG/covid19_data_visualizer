import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import app
from app import co_da, t_da

def _format_array(arr):
        '''Formats the array in array(dict(label: element), dict(label: element)).
        Also capitalizes first letter and replaces underscore with spaces'''
        
        return [{'label': item.replace("_", " ").capitalize() , 'value':item} for item in arr]

        
def _get_common(col1, col2):
        '''Takes twp collumns and returns common elemtents'''
        return np.intersect1d(col1, col2)

#####################  TMP Page  #######################
layout = html.Div([
        dbc.Row([
                dbc.Col(
                        html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Total cases for"),
                                                dcc.Dropdown(id='tmp:trend_dropdown', 
                                                        options=_format_array(_get_common(co_da.get_locations(), t_da.get_locations())), 
                                                        value='Norway'),
                                                dcc.Graph(id='tmp:trend_graph')
                                        ])
                                )
                        ]), width=10)
        ], justify='center'), 
])

@app.callback(
        dash.dependencies.Output('tmp:trend_graph', 'figure'),
        [dash.dependencies.Input('tmp:trend_dropdown', 'value')])
def update_comp_tmp(location):
        '''Updates trend graph with one or several location trends'''
        tm_da_co  = t_da.get_location(location)         # Tmp data for a single location
        avg = t_da.get_loc_group()

        return go.Figure(data = (dict(name="Humidity", x=tm_da_co.index, y=tm_da_co["humidity"]), 
                                dict(name="Max temperature[C]", x=tm_da_co.index, y=tm_da_co["maxtempC"]),
                                dict(name="Min temperature[C]", x=tm_da_co.index, y=tm_da_co["mintempC"]), 
                                dict(name="Average", x=avg.index, y=avg[location])))