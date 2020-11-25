import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

from app import app
from app import co_da

from apps.tools import format_array

layout = html.Div([
        dcc.Graph(id='main:map'),



        html.Br(),
        dbc.Row([
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Cases per million:"),
                                                dcc.Graph(id='main:trend_pr_m_graph')
                                        ])
                                )
                        ]), width=6
                ),
                
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Deaths per million:"),
                                                dcc.Graph(id='main:trend_death_pr_m_graph')
                                        ])
                                )
                        ]), width=6
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

        fig = go.Figure(
                data=c_map
        ).update_layout(
                autosize=True,
                margin=dict(t=0, b=0, l=0, r=0),

                geo = dict(
                        showframe=False
                ) 
        )

        return fig


@app.callback(
        dash.dependencies.Output('main:trend_pr_m_graph', 'figure'),
        dash.dependencies.Output('main:trend_death_pr_m_graph', 'figure'),
        dash.dependencies.Input('main:map', 'clickData'))
def main_locations_per_m(value):
        '''Updates trend graph with one or several location trends'''
        try:
                selected_country = value["points"][0]["location"]
        except:
                selected_country = "NOR"

        lo_da = co_da.get_iso(selected_country)

        total_cases = go.Figure(data = dict(name=selected_country, x=lo_da["date"], y=lo_da["total_cases_per_million"]))
        total_deaths = go.Figure(data = dict(name=selected_country, x=lo_da["date"], y=lo_da["total_deaths_per_million"]))
        return total_cases, total_deaths