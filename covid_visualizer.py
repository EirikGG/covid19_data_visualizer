import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
#import plotly.graph_objs as go
import pandas as pd

from covid_data import Regional_Data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Regional data
reg_data = Regional_Data()
co_da = reg_data.get_total_cases()
fig = px.bar(x=co_da["x"], y=co_da["y"])
fig2 = px.bar(x=co_da["x"], y=co_da["y"])


app.layout = html.Div(children=[
        html.H1(children='COVID-19 data'),
        html.Details([
                html.Summary("Regional data"),
                html.Div(html.Div(children=[
                        dcc.Graph(id='graph1', figure=fig, style={'display': 'inline-block'}), 
                        dcc.Graph(id='graph2', figure=fig2, style={'display': 'inline-block'})
                ]))
        ])
])

if __name__ == '__main__':
        app.run_server(debug=True)
