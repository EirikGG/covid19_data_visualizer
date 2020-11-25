import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

from app import app
from app import co_da, t_da

from apps.tools import format_array

layout = html.Div([
        dbc.Row([
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3(id="main:header"),
                                                dcc.Graph(id='main:map'),
                                        ])
                                )
                        ]), width=12
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
                        ]), width=6
                ),
                
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Total deaths"),
                                                dcc.Graph(id='main:total_deaths')
                                        ])
                                )
                        ]), width=6
                ),
        ]),

        html.Br(),
        dbc.Row([
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                
                                        ])
                                )
                        ]), width=12
                ),
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
def main_locations_per_m(value):
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