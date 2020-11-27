import dash, json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import app
from app import co_da, t_da

from apps.tools import format_array, format_col, get_common

width = 10

layout = html.Div([
        dbc.Row([
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3(id="main:header"),
                                                dcc.Graph(id='main:map'),
                                        ])
                                )
                        ]), width={"size": 5, "offset": 1},
                ),
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Total cases"),
                                                dcc.Graph(id='main:total_cases')
                                        ])
                                )
                        ]), width={"size": 5, "offset": 0},
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
                                                                html.Br(),
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info3"),
                                                                        ])
                                                                ),
                                                        ], width={"size": 4, "offset": 0}),
                                                        dbc.Col([
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info4"),
                                                                        ])
                                                                ),
                                                                html.Br(),
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
                                                        dbc.Col([
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info7"),
                                                                        ])
                                                                ),
                                                                html.Br(),
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info8"),
                                                                        ])
                                                                ),
                                                                html.Br(),
                                                                dbc.Card(
                                                                        dbc.CardBody([
                                                                                html.H5(id="main:info9"),
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
                                                html.H3("Total deaths"),
                                                dcc.Graph(id='main:total_deaths')
                                        ])
                                )
                        ]), width={"size": 5, "offset": 1},
                ),
                
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Total tests"),
                                                dcc.Graph(id='main:total_tests')
                                        ])
                                )
                        ]), width={"size": 5, "offset": 0},
                ),
        ]),
])



# Update map
@app.callback(
        dash.dependencies.Output('main:map', 'figure'),
        dash.dependencies.Input('url', 'pathname'))
def update_map(iso_code):
        iso_total = co_da.get_total_by_iso()

        #       text=[format_col(co_da.get_loc_from_iso(loc)) for loc in iso_total.index],
        c_map = go.Choropleth(
                locations=iso_total.index.get_level_values("iso_code"),
                z=iso_total,
                text=iso_total.index.get_level_values("location"),
                hoverinfo="text"
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
        dash.dependencies.Output('main:total_tests', 'figure'),
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
        total_tests = go.Figure(data = dict(name=selected_country, x=lo_da["date"], y=lo_da["total_tests"]))

        return total_cases, total_deaths, total_tests, full_co_name

@app.callback(
        dash.dependencies.Output('main:info1', 'children'),
        dash.dependencies.Output('main:info2', 'children'),
        dash.dependencies.Output('main:info3', 'children'),
        dash.dependencies.Output('main:info4', 'children'),
        dash.dependencies.Output('main:info5', 'children'),
        dash.dependencies.Output('main:info6', 'children'),
        dash.dependencies.Output('main:info7', 'children'),
        dash.dependencies.Output('main:info8', 'children'),
        dash.dependencies.Output('main:info9', 'children'),
        dash.dependencies.Input('main:map', 'clickData'))
def main_info(click):
        try:
                selected_country = click["points"][0]["location"]
        except:
                selected_country = "NOR"

        cont = co_da.get_iso(selected_country)
        cont = cont[cont["date"].max() == cont["date"]]

        with open("config/text_content.json", "r") as f:
                selected_cols = json.load(f)["general_info_cols"]
                data = []
                for e in selected_cols:
                        column_name = format_col(e["col"])

                        value = cont[e["col"]].values[0]
                        value = round(value, 1) if not np.isnan(value) else "NaN"

                        unit = e["unit"] if str != type(value) else ""

                        data.append("{}: {}{}".format(column_name, value, unit))

        return data

