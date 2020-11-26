import dash, time

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

from app import app
from app import co_da

from apps.tools import format_array, toUnix, toDT, format_marks


#####################  TMP Page  #######################
layout = html.Div([
        dbc.Row([
                dbc.Col(
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Configurable graph:"),
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
                                        html.H6("Date", id="conf:date_label"),
                                        dcc.Slider(
                                                id="conf:slider",
                                                updatemode="drag",
                                                min=toUnix(co_da.get_dates().min()),
                                                max=toUnix(co_da.get_dates().max()),
                                                value=toUnix(co_da.get_dates().max()),
                                        ),
                                        dcc.Graph(id='conf:trend_graph'),
                                ])
                        ), width={"size": 10, "offset": 1},
                )
        ], align='center'),
        html.Br(),
        dbc.Row([                
                dbc.Col(
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Cases per million:"),
                                        dcc.Dropdown(id='conf:trend_pr_m_dropdown', 
                                                options=format_array(co_da.get_locations()), 
                                                value=['Norway', 'Sweden', 'Denmark'], 
                                                multi=True),
                                        dcc.Graph(id='conf:trend_pr_m_graph')
                                ])
                        ), width={"size": 5, "offset": 1},
                ),
                dbc.Col(
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Deaths per million:"),
                                        dcc.Dropdown(id='conf:trend_death_pr_m_dropdown', 
                                                options=format_array(co_da.get_locations()), 
                                                value=['Norway', 'Sweden', 'Denmark'], 
                                                multi=True),
                                        dcc.Graph(id='conf:trend_death_pr_m_graph')
                                ])
                        ), width={"size": 5, "offset": 0},
                )
        ]),
])

        
@app.callback(
        dash.dependencies.Output('conf:trend_graph', 'figure'),
        dash.dependencies.Output('conf:date_label', 'children'),
        
        dash.dependencies.Input('conf:trend_dropdown_x', 'value'),
        dash.dependencies.Input('conf:trend_dropdown_y', 'value'),
        dash.dependencies.Input('conf:trend_dropdown_z', 'value'),
        dash.dependencies.Input('conf:slider', 'value'))
def update_conf_scat(x_axis, y_axis, z_axis, date):
        '''Updates the map with a new x and y axis'''
        # Convert date from unix time to datetime and use to filter date
        date = toDT(date)
        data = co_da.get_date(date)
        data = data["World" != data["location"]]

        fig = go.Scatter()

        print(x_axis, y_axis, z_axis)

        # Creates a figure with custom x and y axis, returns empty figure if one axis is deselected
        if (x_axis and y_axis and not z_axis):
                fig = go.Scatter(x=data[x_axis], 
                                y=data[y_axis],
                                mode="markers",
                                text=data["location"],
                                hoverinfo="text")
        elif (x_axis and y_axis and z_axis):
                fig = go.Scatter3d(x=data[x_axis], 
                                y=data[y_axis],
                                z=data[z_axis],
                                mode="markers",
                                text=data["location"],
                                hoverinfo="text")

        return go.Figure(fig), "Date: {}".format(date)
        
@app.callback(
        dash.dependencies.Output('conf:trend_pr_m_graph', 'figure'),
        [dash.dependencies.Input('conf:trend_pr_m_dropdown', 'value')])
def update_locations_pr_m_cases(locations):
        '''Updates trend graph with one or several location trends'''
        data = []
        for location in (locations,) if str==type(locations) else locations:
                lo_da = co_da.get_location(location)
                data.append(dict(name=location, x=lo_da["date"], y=lo_da["total_cases_per_million"]))
        return go.Figure(data = data)

@app.callback(
        dash.dependencies.Output('conf:trend_death_pr_m_graph', 'figure'),
        [dash.dependencies.Input('conf:trend_death_pr_m_dropdown', 'value')])
def update_locations_pr_m_deaths(locations):
        '''Updates trend graph with one or several location trends'''
        data = []
        for location in (locations,) if str==type(locations) else locations:
                lo_da = co_da.get_location(location)
                data.append(dict(name=location, x=lo_da["date"], y=lo_da["total_deaths_per_million"]))
        return go.Figure(data = data)