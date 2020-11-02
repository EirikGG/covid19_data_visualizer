import dash, json
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from datasets import Covid_Data

def _format_array(arr):
        '''Formats the array in array(dict(label: element), dict(label: element)). Used for dropdown menues'''
        return [{'label': item, 'value':item} for item in arr]


# Variable containg text used in website
texts = json.load(open("text_content.json"))

# Importing and setting theme
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# Importing backends
co_da = Covid_Data()









##################### Figures #######################

# Create regional data
reg_summed = co_da.get_summed_cont()

# Total cases by region (bar chart)
total_by_region = go.Figure(data=(
        go.Bar(name='Total cases', x=reg_summed.index, y=reg_summed["new_cases"]),
        go.Bar(name='Total deaths', x=reg_summed.index, y=reg_summed["new_deaths"])))

# Calculate lethality prosentage for each continent (pie chart)
le_pr_cont_pie = go.Figure(data=go.Pie(labels=reg_summed.index, values=reg_summed["new_deaths"]))







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
                                
                        ], label="Temperature data")
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


# Run webpage
if __name__ == '__main__':
        app.run_server(debug=False, use_reloader=False)