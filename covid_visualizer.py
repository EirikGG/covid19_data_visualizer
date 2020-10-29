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

df = pd.DataFrame({
        "Continent": co_da.index,
        "Total infected": co_da["new_cases"]
})

fig     = px.bar(df, x="Continent", y="Total infected")


app.layout = html.Div(children=[
        html.H1(children='COVID-19 data'),
        html.Details([
                html.Summary('Regional data'),
                html.Div(children=[dcc.Graph(id='graph1', figure=fig, style={'display': 'inline-block'}), 
                                dcc.Graph(id='graph2', figure=fig, style={'display': 'inline-block'}),
                                dcc.Graph(id='graph3', figure=fig, style={'display': 'inline-block'})
                ])
        ], open = True)
])

if __name__ == '__main__':
        app.run_server(debug=True)
