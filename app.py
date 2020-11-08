import dash, json, time
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from sklearn import preprocessing

from datasets import Covid_Data, Tmp_Data

def _format_array(arr):
        '''Formats the array in array(dict(label: element), dict(label: element)).
        Also capitalizes first letter and replaces underscore with spaces'''
        
        return [{'label': item.replace("_", " ").capitalize() , 'value':item} for item in arr]

def _get_common(col1, col2):
        '''Takes twp collumns and returns common elemtents'''
        return np.intersect1d(col1, col2)

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


# Variable containg text used in website
texts = json.load(open("config/text_content.json"))

# Importing and setting theme
external_stylesheets = [dbc.themes.SIMPLEX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

server = app.server

# Importing backends
co_da = Covid_Data()    # Covid data
t_da = Tmp_Data()       # Temperature data





##################### Covid Figures #######################

# Create regional data
reg_summed = co_da.get_summed_cont()

# Total cases by region (bar chart)
total_by_region = go.Figure(data=(go.Bar(name='Total cases', x=reg_summed.index, y=reg_summed["new_cases"])))

# Total cases by region (bar chart)
total_by_region_pr_m = go.Figure(data=(go.Bar(name='Total cases', x=reg_summed.index, y=reg_summed["new_cases_per_million"])))

# Calculate lethality prosentage for each continent (pie chart)
le_pr_cont_pie = go.Figure(data=(go.Bar(name='Total deaths', x=reg_summed.index, y=reg_summed["new_deaths_per_million"], marker={'color':'#ff7f0e'})))



# Webpage main layout
app.layout = html.Div(children=[
        dbc.NavbarSimple(
                children=[
                        dbc.NavItem(dbc.NavLink("Covid-19", href="/")),
                        dbc.NavItem(dbc.NavLink("Temperature", href="/tmp")),
                        dbc.NavItem(dbc.NavLink("Education", href="/edu"))],
                brand="Covid-19 data",
                brand_href="",
                color="primary",
                dark=True,
                sticky="top"),
        dcc.Location(id='url', refresh=False),

        dbc.Card(dbc.CardBody([
                html.Br(),
                html.Div(id="div:page-content"),
                html.Br(),
                html.Div([
                        dbc.Row([
                                dbc.Col(
                                        html.Div([
                                                dbc.Card(
                                                        dbc.CardBody([
                                                                html.P(texts["description"])
                                                        ])
                                                )
                                        ])
                                )
                        ])
                ])
        ])),
])
        
                

##################### Covid Page #######################
covid_page = html.Div([
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
        

        html.Br(),
        dbc.Row([
                dbc.Col(
                        html.Div([
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
                                )
                        ]), width=12
                )
        ], align='center'),
])






#####################  TMP Page  #######################
tmp_page = html.Div([
        dbc.Row([
        dbc.Col(
                html.Div([
                        dbc.Card(
                                dbc.CardBody([
                                        html.H3("Total cases for"),
                                        dcc.Dropdown(id='tmp:trend_dropdown', 
                                                options=_format_array(_get_common(co_da.get_locations(), t_da.get_locations())), 
                                                value='Norway'),
                                        dcc.Graph(id='tmp:trend_graph')
                                ])
                        )
                ]), width=12)
        ], align='center'), 
])


                
# Update the index
@app.callback(dash.dependencies.Output('div:page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(path):
        if '/' == path:
                return covid_page
        elif '/tmp' == path:
                return tmp_page
        elif '/edu' == path:
                pass
        else:
                return html.Div([html.H1("Error 404: page {} not found".format(path))])



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
        dash.dependencies.Output('tmp:trend_graph', 'figure'),
        [dash.dependencies.Input('tmp:trend_dropdown', 'value')])
def update_comp_tmp(location):
        '''Updates trend graph with one or several location trends'''
        tm_da_co  = t_da.get_location(location)         # Tmp data for a single location
        avg = t_da.get_loc_group()

        return go.Figure(data = (dict(name="Humidity", x=tm_da_co.index, y=tm_da_co["humidity"]), 
                                dict(name="Max temperature[C]", x=tm_da_co.index, y=tm_da_co["maxtempC"]),
                                dict(name="Min temperature[C]", x=tm_da_co.index, y=tm_da_co["mintempC"]), 
                                dict(name="Average", x=avg.index, y=avg[location])))

# Run webpage
if __name__ == '__main__':
        app.run_server(debug=False, use_reloader=False)