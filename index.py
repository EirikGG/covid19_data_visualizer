import dash, json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import app, co_da
from apps import main, configurable, predictions, continent


server = app.server

# Webpage main layout
app.layout = html.Div(children=[
        dbc.NavbarSimple(
                children=[
                        dbc.NavItem(dbc.NavLink("Home", href="/")),
                        dbc.NavItem(dbc.NavLink("Continent", href="/continent")),
                        dbc.NavItem(dbc.NavLink("Predictions", href="/predictions")),
                        dbc.NavItem(dbc.NavLink("Configurable", href="/configurable"))],
                brand="Covid-19 data",
                brand_href="/",
                color="primary",
                dark=True,
                sticky="top"),
        dcc.Location(id='url', refresh=False),

        html.Div(id="div:warning_dataset"),
        html.Div(id="div:warning_predictions"),

        dbc.Container([
                        html.Br(),
                        html.Div(id="div:page-content"),
                        html.Br(),
        ], fluid=True)
])
                
# Update the index
@app.callback(dash.dependencies.Output('div:page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(path):
        if '/' == path:
                return main.layout
        elif '/continent' == path:
                return continent.layout
        elif '/predictions' == path:
                return predictions.layout
        elif '/configurable' == path:
                return configurable.layout
        else:
                return html.Div([html.H1("Error 404: page {} not found".format(path))])

# Update warning
@app.callback(
        dash.dependencies.Output('div:warning_dataset', 'children'),
        dash.dependencies.Output('div:warning_predictions', 'children'),
        dash.dependencies.Input('url', 'pathname'))
def update_warnings(path):
        with open("config/text_content.json", "r") as f:
                warnings = json.load(f)["warnings"]

                dataset = dbc.Alert([
                        warnings["dataset"]
                ], color="warning") if "local file" == co_da.get_description() else None

                predictions = dbc.Alert([
                        warnings["predictions"]
                ], color="warning") if "/predictions" == path else None

        return dataset, predictions

# Run webpage
if __name__ == '__main__':
        app.run_server(debug=False, use_reloader=False)