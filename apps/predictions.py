import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import app
from app import co_da, t_da

from apps.tools import format_array, get_common

#####################  TMP Page  #######################
layout = html.Div([
        dbc.Row([
                dbc.Col(
                        html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Total cases for"),
                                                dcc.Dropdown(id='tmp:trend_dropdown', 
                                                        options=format_array(get_common(co_da.get_locations(), t_da.get_locations())), 
                                                        value='Norway'),
                                                dcc.Graph(id='tmp:trend_graph')
                                        ])
                                )
                        ]), width={"size": 10, "offset": 0},
                )
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