import dash, json
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from sklearn import preprocessing

from datasets import Covid_Data, Tmp_Data

def _format_array(arr):
        '''Formats the array in array(dict(label: element), dict(label: element)). Used for dropdown menues'''
        return [{'label': item, 'value':item} for item in arr]

def _get_common(col1, col2):
        '''Takes twp collumns and returns common elemtents'''
        return np.intersect1d(col1, col2)

def _normalize(col):
        '''Takes a pandas column and normalizes the values'''
        # https://stackoverflow.com/questions/48823400/pandas-series-to-2d-array
        col = pd.DataFrame(col.values.tolist())
        
        # https://chrisalbon.com/python/data_wrangling/pandas_normalize_column/
        x = col.astype(float)                           # Creates a new array of floats 
        min_max_scaler = preprocessing.MinMaxScaler()   # Creates a min/max object
        x_scaled = min_max_scaler.fit_transform(x)      # Fit column
        return pd.DataFrame(x_scaled)                   # Returns normalized result as df


# Variable containg text used in website
texts = json.load(open("config/text_content.json"))

# Importing and setting theme
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# Importing backends
co_da = Covid_Data()    # Covid data
t_da = Tmp_Data()       # Temperature data









##################### Covid Figures #######################

# Create regional data
reg_summed = co_da.get_summed_cont()

# Total cases by region (bar chart)
total_by_region = go.Figure(data=(
        go.Bar(name='Total cases', x=reg_summed.index, y=reg_summed["new_cases"]),
        go.Bar(name='Total deaths', x=reg_summed.index, y=reg_summed["new_deaths"])))

# Calculate lethality prosentage for each continent (pie chart)
le_pr_cont_pie = go.Figure(data=go.Pie(labels=reg_summed.index, values=reg_summed["new_deaths"]))







#####################  TMP Figures  #######################

# Temperature for norway
total_by_region = go.Figure(data=(
        go.Bar(name='Total cases', x=reg_summed.index, y=reg_summed["new_cases_per_million"]),
        go.Bar(name='Total deaths', x=reg_summed.index, y=reg_summed["new_deaths_per_million"])))






#####################  Edu Figures  #######################






# Webpage main layout
app.layout = html.Div(children=[
        dbc.Navbar([
                dbc.Row([
                        dbc.Col(html.H1("Covid-19 data", style={"color":"#FFFFFF"}))
                ])
        ], color="#404040", sticky="top"),

            
        dbc.Card(dbc.CardBody([
                dcc.Tabs([
                        dcc.Tab([
                                ##################### Covid Page #######################
                                html.Br(),
                                dbc.Row([
                                        dbc.Col(html.Div([
                                                        dbc.Card(
                                                                dbc.CardBody([
                                                                        html.H3("Total cases and deaths by continents:"),
                                                                        dcc.Graph(id='reg:comparison', figure=total_by_region)
                                                                ])
                                                        )
                                                ]), width=7),
                                        dbc.Col(html.Div([
                                                        dbc.Card(
                                                                dbc.CardBody([
                                                                        html.H3("Death comparison:"),
                                                                        dcc.Graph(id='reg:deaths', figure=le_pr_cont_pie)
                                                                ])
                                                        )
                                                ]), width=5)
                                ], align='center'),
                                
                                html.Br(),
                                dbc.Row([
                                        dbc.Col(
                                                html.Div([
                                                        dbc.Card(
                                                                dbc.CardBody([
                                                                        html.H3("Total cases for:"),
                                                                        dcc.Dropdown(id='loc:trend_dropdown', 
                                                                                options=_format_array(co_da.get_locations()), 
                                                                                value=['Norway', 'Sweden', 'Denmark'], 
                                                                                multi=True),
                                                                        dcc.Graph(id='loc:trend_graph')
                                                                ])
                                                        )
                                                ]), width=12)
                                        ], align='center'),
                        ], label="Regional data"),






                        dcc.Tab([
                                #####################  TMP Page  #######################
                                html.Br(),
                                dbc.Row([
                                        dbc.Col(
                                                html.Div([
                                                        dbc.Card(
                                                                dbc.CardBody([
                                                                        html.H3("Total cases for:"),
                                                                        dcc.Dropdown(id='tmp:trend_dropdown', 
                                                                                options=_format_array(_get_common(co_da.get_locations(), t_da.get_locations())), 
                                                                                value='Norway'),
                                                                        dcc.Graph(id='tmp:trend_graph')
                                                                ])
                                                        )
                                                ]), width=12)
                                        ], align='center'),
                        ], label="Temperature data"),










                        dcc.Tab([
                        #####################  Edu Page  #######################
                                
                        ], label="Educational data")
                ]),

                html.Br(),
                dbc.Card(dbc.CardBody([
                        html.P(texts["description"])
                ]))
        ]))
])



@app.callback(
        dash.dependencies.Output('loc:trend_graph', 'figure'),
        [dash.dependencies.Input('loc:trend_dropdown', 'value')])
def update_locations(locations):
        '''Updates trend graph with one or several location trends'''
        data = []
        for location in (locations,) if str==type(locations) else locations:
                lo_da = co_da.get_location(location)
                data.append(dict(name=location, x=lo_da["date"], y=lo_da["total_cases"]))
        return go.Figure(data = data)




@app.callback(
        dash.dependencies.Output('tmp:trend_graph', 'figure'),
        [dash.dependencies.Input('tmp:trend_dropdown', 'value')])
def update_comp_tmp(location):
        '''Updates trend graph with one or several location trends'''
        
        tm_da_co  = t_da.get_location(location)         # Tmp data for a single location

        return go.Figure(data = (dict(name="Humidity", x=tm_da_co.index, y=tm_da_co["humidity"]), 
                                dict(name="Max temperature[C]", x=tm_da_co.index, y=tm_da_co["maxtempC"]), 
                                dict(name="Min temperature[C]", x=tm_da_co.index, y=tm_da_co["mintempC"])))







# Run webpage
if __name__ == '__main__':
        app.run_server(debug=False, use_reloader=False)