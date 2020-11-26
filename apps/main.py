import dash, json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

from app import app
from app import co_da, t_da

from apps.tools import format_array, format_col, get_common

layout = html.Div([
        dbc.Row([
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3(id="main:header"),
                                                dcc.Graph(id='main:map'),
                                        ])
                                )
                        ]), width={"size": 10, "offset": 1},
                ),
        ]),

        html.Br(),
        dbc.Row([
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("General information"),
                                                html.Br(),
                                                dbc.Row([
                                                        dbc.Col([
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info1"),
                                                                        ])
                                                                ),
                                                                html.Br(),
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info2"),
                                                                        ])
                                                                ),
                                                        ], width={"size": 4, "offset": 0}),
                                                        dbc.Col([
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info3"),
                                                                        ])
                                                                ),
                                                                html.Br(),
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info4"),
                                                                        ])
                                                                ),
                                                        ], width={"size": 4, "offset": 0}),
                                                        dbc.Col([
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info5"),
                                                                        ])
                                                                ),
                                                                html.Br(),
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info6"),
                                                                        ])
                                                                ),
                                                        ], width={"size": 4, "offset": 0}),
                                                ])
                                        ])
                                )
                        ]), width={"size": 10, "offset": 1},
                ),
        ]),

        html.Br(),
        dbc.Row([
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Total cases"),
                                                dcc.Graph(id='main:total_cases')
                                        ])
                                )
                        ]), width={"size": 5, "offset": 1},
                ),
                
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Total deaths"),
                                                dcc.Graph(id='main:total_deaths')
                                        ])
                                )
                        ]), width={"size": 5, "offset": 0},
                ),
        ]),
        html.Br(),
        dbc.Row([
                dbc.Col(
                        html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Temperature"),
                                                dcc.Graph(id='main:temperature')
                                        ])
                                )
                        ]), width={"size": 10, "offset": 1},
                )
        ]), 
])



# Update map
@app.callback(
        dash.dependencies.Output('main:map', 'figure'),
        dash.dependencies.Input('main:map', 'clickData'))
def update_map(iso_code):
        print("User clicked country with iso code = \"{}\" ".format(iso_code))
        iso_total = co_da.get_total_by_iso()

        c_map = go.Choropleth(
                locations=iso_total.index,
                z=iso_total
        )

        return go.Figure(
                data=c_map
        ).update_layout(
                autosize=True,
                margin=dict(
                        t=0, b=0, l=0, r=0),
                geo = dict(
                        showframe=False)
        )


@app.callback(
        dash.dependencies.Output('main:total_cases', 'figure'),
        dash.dependencies.Output('main:total_deaths', 'figure'),
        dash.dependencies.Output('main:header', 'children'),
        dash.dependencies.Input('main:map', 'clickData'))
def main_locations(value):
        '''Updates trend graph with one or several location trends'''
        try:
                selected_country = value["points"][0]["location"]
        except:
                selected_country = "NOR"

        lo_da = co_da.get_iso(selected_country)
        
        full_co_name = "Selected country: {}".format(lo_da["location"].values[0])

        total_cases = go.Figure(data = dict(name=selected_country, x=lo_da["date"], y=lo_da["total_cases"]))
        total_deaths = go.Figure(data = dict(name=selected_country, x=lo_da["date"], y=lo_da["total_deaths"]))

        return total_cases, total_deaths, full_co_name

@app.callback(
        dash.dependencies.Output('main:info1', 'children'),
        dash.dependencies.Output('main:info2', 'children'),
        dash.dependencies.Output('main:info3', 'children'),
        dash.dependencies.Output('main:info4', 'children'),
        dash.dependencies.Output('main:info5', 'children'),
        dash.dependencies.Output('main:info6', 'children'),
        dash.dependencies.Input('main:map', 'clickData'))
def main_info(value):
        try:
                selected_country = value["points"][0]["location"]
        except:
                selected_country = "NOR"

        cont = co_da.get_iso(selected_country)
        cont = cont[cont["date"].max() == cont["date"]]

        with open("config/text_content.json", "r") as f:
                selected_cols = json.load(f)["general_info"]

        return ["{}: {}".format(format_col(col), *cont[col].values) for col in selected_cols]
        

@app.callback(
        dash.dependencies.Output('main:temperature', 'figure'),
        dash.dependencies.Input('main:map', 'clickData'))
def main_temp(location):
        '''Updates trend graph with one location trends'''
        try:
                selected_country = value["points"][0]["location"]
        except:
                selected_country = "NOR"
        location = co_da.get_loc_from_iso(selected_country)
        tm_da_co  = t_da.get_location(location)         # Tmp data for a single location
        avg = t_da.get_loc_group()

        return go.Figure(data = (dict(name="Humidity", x=tm_da_co.index, y=tm_da_co["humidity"]), 
                                dict(name="Max temperature[C]", x=tm_da_co.index, y=tm_da_co["maxtempC"]),
                                dict(name="Min temperature[C]", x=tm_da_co.index, y=tm_da_co["mintempC"]), 
                                dict(name="Average", x=avg.index, y=avg[location])))