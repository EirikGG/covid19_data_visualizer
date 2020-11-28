import dash, json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import app
from app import co_da, t_da
from apps.tools import format_array, get_common, format_cols


layout = html.Div([
        dbc.Row([
                dbc.Col(
                        html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Feature ranking using lasso regression"),
                                                dbc.Col([
                                                        dcc.Dropdown(id='pred:feature', 
                                                                options=format_array(json.load(open("config/dataset.json"))["regression"]["features"]),
                                                                value="total_cases"
                                                        )
                                                ]),
                                                dcc.Graph(id='pred:table')
                                        ])
                                )
                        ]), width={"size": 10, "offset": 0},
                )
        ], justify='center'), 
])

@app.callback(
        dash.dependencies.Output('pred:table', 'figure'),
        dash.dependencies.Input('pred:feature', 'value'))
def pred_table(value):
        data = co_da.get_feature_ranking(value)
        
        tab = go.Table(
                header=dict(values=list(format_cols(data.columns))),
                cells=dict(values=[format_cols(data["features"]), data["coeff"]]),
        )
        
        return go.Figure(tab)