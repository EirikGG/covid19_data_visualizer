import dash, time, json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

from app import app
from app import co_da, t_da

from apps.tools import format_array, format_col


#####################  TMP Page  #######################
layout = html.Div([
        dbc.Row([
                dbc.Col(
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Configurable scatter plot:"),
                                        html.Br(),
                                        dbc.Row([
                                                dbc.Col([
                                                        html.H6("X-Axis:"),
                                                        dcc.Dropdown(id='conf:trend_dropdown_x', 
                                                                options=format_array(co_da.get_cols()),
                                                                value="population")
                                                ]),
                                                dbc.Col([
                                                        html.H6("Y-Axis:"),
                                                        dcc.Dropdown(id='conf:trend_dropdown_y', 
                                                                options=format_array(co_da.get_cols()),
                                                                value="total_cases")                                                                                        
                                                ]),
                                                dbc.Col([
                                                        html.H6("Z-Axis:"),
                                                        dcc.Dropdown(id='conf:trend_dropdown_z', 
                                                                options=format_array(co_da.get_cols()),
                                                                value="")                                                                                        
                                                ]),
                                        ]),
                                        html.Br(),
                                        html.H6("Date"),
                                        dcc.DatePickerSingle(
                                                id='conf:date',
                                                min_date_allowed=co_da.get_dates().min(),
                                                max_date_allowed=co_da.get_dates().max(),
                                                date=co_da.get_dates().max()
                                        ),
                                        dcc.Graph(id='conf:trend_graph'),
                                ])
                        ), width={"size": 5, "offset": 1},
                ),
                dbc.Col(
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Filter location:"),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        dbc.Row([
                                                dbc.Col([
                                                        html.H6("Column:"),
                                                        dcc.Dropdown(id='conf:filter_col_dropdown', 
                                                                options=format_array(json.load(open("config/dataset.json"))["regression"]["features"]),
                                                                value="population")
                                                ]),
                                                dbc.Col([
                                                        html.H6("Operator:"),
                                                        dcc.Dropdown(id='conf:filter_operator_dropdown', 
                                                                options=[
                                                                        {'label': "Equals", 'value':"equals"},
                                                                        {'label': "Greater than", 'value':"greater"},
                                                                        {'label': "Less than", 'value':"less"},
                                                                ],
                                                                value="less")                                                                                        
                                                ]),
                                                dbc.Col([
                                                        html.H6("Value:"),
                                                        dcc.Input(
                                                                id='conf:filter_value',
                                                                type="number",
                                                                value=10000)
                                                ])
                                        ]),
                                        html.Br(),
                                        html.Br(),
                                        dcc.Graph(id='conf:filter_tables'),
                                ])
                        ), width={"size": 5, "offset": 0},
                )
        ], align='center'),
        html.Br(),
        dbc.Row([                
                dbc.Col(
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Compare countries:"),
                                        html.Br(),
                                        dbc.Row([
                                                dbc.Col([
                                                        html.H6("Country:"),
                                                        dcc.Dropdown(id='conf:trend_pr_m_dropdown', 
                                                                options=format_array(co_da.get_locations()), 
                                                                value=['Norway', 'Sweden', 'Denmark'], 
                                                                multi=True),
                                                ]),
                                                dbc.Col([
                                                        html.H6("Column:"),
                                                        dcc.Dropdown(id='conf:column_dropdown', 
                                                                options=format_array(co_da.get_cols()),
                                                                value="total_cases")                                                                                        
                                                ]),
                                        ]),
                                        dcc.Graph(id='conf:trend')
                                ])
                        ), width={"size": 10, "offset": 1},
                ),
        ]),
])

        
@app.callback(
        dash.dependencies.Output('conf:trend_graph', 'figure'),
        
        dash.dependencies.Input('conf:trend_dropdown_x', 'value'),
        dash.dependencies.Input('conf:trend_dropdown_y', 'value'),
        dash.dependencies.Input('conf:trend_dropdown_z', 'value'),
        dash.dependencies.Input('conf:date', 'date'))
def update_conf_scat(x_axis, y_axis, z_axis, date):
        '''Updates the map with a new x and y axis'''
        data = co_da.get_date(date)
        data = data["World" != data["location"]]

        fig = go.Scatter()

        if (x_axis and y_axis and not z_axis):
                fig = go.Figure(go.Scatter(x=data[x_axis], 
                                y=data[y_axis],
                                mode="markers",
                                text=data["location"],
                                hoverinfo="text")).update_layout(
                                       xaxis=dict(
                                                title=format_col(x_axis)
                                        ),
                                        yaxis=dict(
                                                title=format_col(y_axis)
                                        ) 
                                )
        elif (x_axis and y_axis and z_axis):
                fig = go.Figure(go.Scatter3d(x=data[x_axis], 
                                y=data[y_axis],
                                z=data[z_axis],
                                mode="markers",
                                text=data["location"],
                                hoverinfo="text")).update_layout(
                                scene = dict(
                                        xaxis_title=format_col(x_axis),
                                        yaxis_title=format_col(y_axis),
                                        zaxis_title=format_col(z_axis))
                                )

        return fig
         
@app.callback(
        dash.dependencies.Output('conf:trend', 'figure'),
        dash.dependencies.Input('conf:trend_pr_m_dropdown', 'value'),
        dash.dependencies.Input('conf:column_dropdown', 'value'))
def conf_trend(locations, col):
        '''Updates trend graph with one or several location trends'''
        data = []
        for location in (locations,) if str==type(locations) else locations:
                lo_da = co_da.get_location(location)
                data.append(dict(name=location, x=lo_da["date"], y=lo_da[col]))
        return go.Figure(data = data)
         
@app.callback(
        dash.dependencies.Output('conf:filter_tables', 'figure'),
        dash.dependencies.Input('conf:filter_col_dropdown', 'value'),
        dash.dependencies.Input('conf:filter_operator_dropdown', 'value'),
        dash.dependencies.Input('conf:filter_value', 'value'))
def conf_filtered(col, operator, value):
        '''Filters location and returns a table of the locations'''
        
        tmp_feature_name = "average_temperature"
        if not tmp_feature_name in co_da.get_data():
                co_da.add_tmp(tmp_feature_name, t_da.get_avg)
        data = co_da.get_filtered_data_loc(col, operator, value)
        
        tab = go.Table(
                cells=dict(values=[data]),
        )
        
        return go.Figure(tab) if col and operator and value else go.Figure()