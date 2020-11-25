import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import app, co_da
from apps import main, configurable, temperature


server = app.server

# Webpage main layout
app.layout = html.Div(children=[
        dbc.NavbarSimple(
                children=[
                        dbc.NavItem(dbc.NavLink("Home", href="/")),
                        dbc.NavItem(dbc.NavLink("Configurable", href="/conf"))],
                brand="Covid-19 data",
                brand_href="/",
                color="primary",
                dark=True,
                sticky="top"),
        dcc.Location(id='url', refresh=False),
        html.Div(id="div:warning"),
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
        elif '/tmp' == path:
                return temperature.layout
        elif '/conf' == path:
                return configurable.layout
        else:
                return html.Div([html.H1("Error 404: page {} not found".format(path))])

# Update warning
@app.callback(dash.dependencies.Output('div:warning', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def update_warning(path):
        return dbc.Alert([
                "Loaded dataset was last updated 19.10.2020"
        ], color="warning") if "local file" == co_da.get_description() else None

# Run webpage
if __name__ == '__main__':
        app.run_server(debug=True, use_reloader=True)