import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from app import app
from app import co_da
from apps.tools import format_array

layout = html.Div([
        dbc.Row([
                dbc.Col(
                        html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Total cases per million"),
                                                dcc.Graph(id='cont:tot_cases')
                                        ])
                                )
                        ]), width={"size": 5, "offset": 0},
                ),
                dbc.Col(
                        html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Total deaths per million"),
                                                dcc.Graph(id='cont:tot_deaths')
                                        ])
                                )
                        ]), width={"size": 5, "offset": 0},
                ),
        ], justify='center'),
        html.Br(),
        dbc.Row([
                dbc.Col(
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Compare continents:"),
                                        html.Br(),
                                        dbc.Row([
                                            dbc.Col([
                                                    html.H6("Continent:"),
                                                    dcc.Dropdown(id='cont:trend_dropdown', 
                                                            options=format_array(co_da.get_conts()), 
                                                            value=['Europe', 'Asia', 'South America', 'Oceania', 'North America', 'Africa'], 
                                                            multi=True),
                                            ]),
                                            dbc.Col([
                                                    html.H6("Column:"),
                                                    dcc.Dropdown(id='cont:col_dropdown', 
                                                            options=format_array(co_da.get_cols()), 
                                                            value="total_cases"),
                                            ]),
                                        ]),
                                        dcc.Graph(id='cont:trend')
                                ])
                        ), width={"size": 10, "offset": 0},
                ),
        ], justify='center'), 
])

@app.callback(
    dash.dependencies.Output('cont:tot_cases', 'figure'),
    dash.dependencies.Output('cont:tot_deaths', 'figure'),
    dash.dependencies.Input('url', 'pathname'))
def pred_table(value):
    reg_summed = co_da.get_tot_pr_m_cont()

    # Total cases by region (bar chart)
    cases_pr_m = go.Figure(data=(go.Bar(name='Total cases', x=reg_summed.index, y=reg_summed["total_cases_per_million"])))

    # Total cases by region (bar chart)
    deaths_pr_m = go.Figure(data=(go.Bar(name='Total deaths', x=reg_summed.index, y=reg_summed["total_deaths_per_million"])))

    return cases_pr_m, deaths_pr_m
        
@app.callback(
        dash.dependencies.Output('cont:trend', 'figure'),
        dash.dependencies.Input('cont:trend_dropdown', 'value'),
        dash.dependencies.Input('cont:col_dropdown', 'value'))
def cont_trend(locations, col):
        '''Updates trend graph with one or several location trends'''
        data = []
        for location in (locations,) if str==type(locations) else locations:
                lo_da = co_da.get_cont(location)
                data.append(dict(name=location, x=lo_da.index, y=lo_da[col]))
        return go.Figure(data = data)