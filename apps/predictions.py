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
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Prediction:"),
                                        html.Br(),
                                        dbc.Row([
                                                dbc.Col([
                                                        html.H6("Country:"),
                                                        dcc.Dropdown(id='pred:country_dropdown', 
                                                                options=format_array(co_da.get_locations()), 
                                                                value='Norway'),
                                                ]),
                                                dbc.Col([
                                                        html.H6("Column:"),
                                                        dcc.Dropdown(id='pred:column_dropdown', 
                                                                options=format_array(json.load(open("config/dataset.json"))["pred"]["cols"]),
                                                                value="total_cases")
                                                ]),
                                                dbc.Col([
                                                        html.H6("Days:"),
                                                        dcc.Input(
                                                                id='pred:days',
                                                                type="number",
                                                                value=100)
                                                ])
                                        ]),
                                        dcc.Graph(id='pred:trend')
                                ])
                        ), width={"size": 10, "offset": 1},
                ),
        ]),
        html.Br(),
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
        tmp_feature_name = "average_temperature"
        if not tmp_feature_name in co_da.get_data():
                co_da.add_tmp(tmp_feature_name, t_da.get_avg)
        
        data = co_da.get_feature_ranking(value)
        
        tab = go.Table(
                header=dict(values=list(format_cols(data.columns))),
                cells=dict(values=[format_cols(data["features"]), data["coeff"]]),
        )
        
        return go.Figure(tab)


@app.callback(
        dash.dependencies.Output('pred:trend', 'figure'),
        dash.dependencies.Input('pred:country_dropdown', 'value'),
        dash.dependencies.Input('pred:column_dropdown', 'value'),
        dash.dependencies.Input('pred:days', 'value'))
def pred_trend(loc, col, days):
        og = co_da.get_location(loc)
        pred = co_da.get_pred_v2(loc, col, days=days)


        fig = go.Figure([
                dict(
                        name="Prediction",
                        x=pred.index,
                        y=pred[0].values
                ),
                dict(
                        name="Original",
                        x=og["date"],
                        y=og[col].values
                ),
        ])

        return fig