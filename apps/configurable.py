import dash, time

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

from app import app
from app import co_da


def _format_array(arr):
        '''Formats the array in array(dict(label: element), dict(label: element)).
        Also capitalizes first letter and replaces underscore with spaces'''
        
        return [{'label': item.replace("_", " ").capitalize() , 'value':item} for item in arr]
# The 3 following functions used for slider convertion:
# https://stackoverflow.com/questions/51063191/date-slider-with-plotly-dash-does-not-work
def _toUnix(t):
        '''Converts datetime to unix time'''
        return int(time.mktime(t.timetuple()))

def _toDT(unix):
        '''Converts unix time to date'''
        return pd.to_datetime(unix, unit='s').date().strftime("%d/%m/%y")

def _format_marks(dTimes):
        '''Formats marks for slider object'''
        unixT = dict()
        for time in dTimes:
                unixT[_toUnix(time)] = str(time.strftime('%d-%m-%y'))
        return unixT

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
                                                        dcc.Dropdown(id='con:trend_dropdown_x', 
                                                                options=_format_array(co_da.get_cols()),
                                                                value="population")
                                                ]),
                                                dbc.Col([
                                                        html.H6("Y-Axis:"),
                                                        dcc.Dropdown(id='con:trend_dropdown_y', 
                                                                options=_format_array(co_da.get_cols()),
                                                                value="total_cases")                                                                                        
                                                ]),
                                        ]),
                                        html.Br(),
                                        html.H6("Date", id="con:date_label"),
                                        dcc.Slider(
                                                id="con:slider",
                                                updatemode="drag",
                                                min=_toUnix(co_da.get_dates().min()),
                                                max=_toUnix(co_da.get_dates().max()),
                                                value=_toUnix(co_da.get_dates().max()),
                                        ),
                                        dcc.Graph(id='con:trend_graph'),
                                ])
                        ), width=12
                )
        ], align='center'),
        html.Br(),
        dbc.Row([                
                dbc.Col(
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Cases per million:"),
                                        dcc.Dropdown(id='loc:trend_pr_m_dropdown', 
                                                options=_format_array(co_da.get_locations()), 
                                                value=['Norway', 'Sweden', 'Denmark'], 
                                                multi=True),
                                        dcc.Graph(id='loc:trend_pr_m_graph')
                                ])
                        ), width=6
                ),
                dbc.Col(
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Deaths per million:"),
                                        dcc.Dropdown(id='loc:trend_death_pr_m_dropdown', 
                                                options=_format_array(co_da.get_locations()), 
                                                value=['Norway', 'Sweden', 'Denmark'], 
                                                multi=True),
                                        dcc.Graph(id='loc:trend_death_pr_m_graph')
                                ])
                        ), width=6
                )
        ]),
])

        
@app.callback(
        dash.dependencies.Output('con:trend_graph', 'figure'),
        dash.dependencies.Output('con:date_label', 'children'),
        [dash.dependencies.Input('con:trend_dropdown_x', 'value'),
        dash.dependencies.Input('con:trend_dropdown_y', 'value'),
        dash.dependencies.Input('con:slider', 'value')])
def update_conf_scat(x_axis, y_axis, date):
        '''Updates the map with a new x and y axis'''
        # Convert date from unix time to datetime and use to filter date
        date = _toDT(date)
        data = co_da.get_date(date)
        data = data["World" != data["location"]]

        # Creates a figure with custom x and y axis, returns empty figure if one axis is deselected
        fig = go.Figure(go.Scatter(x=data[x_axis], 
                                y=data[y_axis], 
                                mode="markers",
                                text=data["location"],
                                hoverinfo="text") if (x_axis and y_axis) else None)

        return fig, "Date: {}".format(date)
        
@app.callback(
        dash.dependencies.Output('loc:trend_pr_m_graph', 'figure'),
        [dash.dependencies.Input('loc:trend_pr_m_dropdown', 'value')])
def update_locations_pr_m_cases(locations):
        '''Updates trend graph with one or several location trends'''
        data = []
        for location in (locations,) if str==type(locations) else locations:
                lo_da = co_da.get_location(location)
                data.append(dict(name=location, x=lo_da["date"], y=lo_da["total_cases_per_million"]))
        return go.Figure(data = data)

@app.callback(
        dash.dependencies.Output('loc:trend_death_pr_m_graph', 'figure'),
        [dash.dependencies.Input('loc:trend_death_pr_m_dropdown', 'value')])
def update_locations_pr_m_deaths(locations):
        '''Updates trend graph with one or several location trends'''
        data = []
        for location in (locations,) if str==type(locations) else locations:
                lo_da = co_da.get_location(location)
                data.append(dict(name=location, x=lo_da["date"], y=lo_da["total_deaths_per_million"]))
        return go.Figure(data = data)