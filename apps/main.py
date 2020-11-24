import dash

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
##################### Covid Figures #######################

# Create regional data
reg_summed = co_da.get_summed_cont()

# Total cases by region (bar chart)
total_by_region = go.Figure(data=(go.Bar(name='Total cases', x=reg_summed.index, y=reg_summed["new_cases"])))

# Total cases by region (bar chart)
total_by_region_pr_m = go.Figure(data=(go.Bar(name='Total cases', x=reg_summed.index, y=reg_summed["new_cases_per_million"])))

# Calculate lethality prosentage for each continent (pie chart)
le_pr_cont_pie = go.Figure(data=(go.Bar(name='Total deaths', x=reg_summed.index, y=reg_summed["new_deaths_per_million"], marker={'color':'#ff7f0e'})))




##################### Covid Page #######################
layout = html.Div([
        dcc.Graph(id='map:map'),



        html.Br(),
        dbc.Row([
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Cases per million"),
                                                html.Br(),
                                                html.Br(),
                                                dcc.Graph(id='reg:comparison', figure=total_by_region_pr_m)
                                        ])
                                )
                        ]), width=4
                ),
                
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Cases per million:"),
                                                dcc.Dropdown(id='loc:trend_pr_m_dropdown', 
                                                        options=_format_array(co_da.get_locations()), 
                                                        value=['Norway', 'Sweden', 'Denmark'], 
                                                        multi=True),
                                                dcc.Graph(id='loc:trend_pr_m_graph')
                                        ])
                                )
                        ]), width=8
                ),
        ]),

        html.Br(),        
        dbc.Row([
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Deaths per million"),
                                                html.Br(),
                                                html.Br(),
                                                dcc.Graph(id='reg:deaths', figure=le_pr_cont_pie)
                                        ])
                                )
                        ]), width=4
                ),
                
                dbc.Col(html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Deaths per million:"),
                                                dcc.Dropdown(id='loc:trend_death_pr_m_dropdown', 
                                                        options=_format_array(co_da.get_locations()), 
                                                        value=['Norway', 'Sweden', 'Denmark'], 
                                                        multi=True),
                                                dcc.Graph(id='loc:trend_death_pr_m_graph')
                                        ])
                                )
                        ]), width=8
                ),
        ]),
])

# Update map
@app.callback(
        dash.dependencies.Output('map:map', 'figure'),
        [dash.dependencies.Input('map:map', 'clickData')])
def update_map(value):
        iso_total = co_da.get_total_by_iso()

        try:
                selected_country = value["points"][0]["location"]
        except:
                selected_country = "NOR"
 
        print(selected_country)

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