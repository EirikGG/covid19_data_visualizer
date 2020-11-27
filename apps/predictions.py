import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import app
from app import co_da, t_da
from sklearn.linear_model import Lasso
from apps.tools import format_array, get_common


layout = html.Div([
        dbc.Row([
                dbc.Col(
                        html.Div([
                                dbc.Card(
                                        dbc.CardBody([
                                                html.H3("Total cases for"),
                                                dcc.Dropdown(id='pred:loc_dropdown', 
                                                        options=format_array(get_common(co_da.get_locations(), t_da.get_locations())), 
                                                        value='Norway'),
                                                dcc.Graph(id='pred:table')
                                        ])
                                )
                        ]), width={"size": 10, "offset": 0},
                )
        ], justify='center'), 
])

@app.callback(
        dash.dependencies.Output('pred:table', 'figure'),
        [dash.dependencies.Input('pred:loc_dropdown', 'value')])
def pred_table(location):
        features = ['new_tests', 'total_tests', 'new_tests_smoothed', 'tests_per_case', 'positive_rate', 
                        'tests_units', 'stringency_index', 'population', 'population_density', 'median_age', 'aged_65_older',
                        'aged_70_older', 'gdp_per_capita', 'extreme_poverty', 'cardiovasc_death_rate', 'diabetes_prevalence', 
                        'female_smokers', 'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand',
                        'life_expectancy', 'human_development_index']

        
        
        return go.Figure(go.Table())