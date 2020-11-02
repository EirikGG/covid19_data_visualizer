import dash, json
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from covid_data import Regional_Data, Location_Data

def _wrap_fig(fig, title):
        '''Wraps the figure in a div, card, cardbody, and a graph
        https://stackoverflow.com/questions/63592900/plotly-dash-how-to-design-the-layout-using-dash-bootstrap-components'''
        return html.Div([
                dbc.Card(
                        dbc.CardBody([
                                html.H3(title),
                                dcc.Graph(id=title, figure=fig)
                        ])
                )
        ])

def _update_layout(fig):
        '''Updates the figure layout'''
        return fig#.update_layout(template='plotly_dark', 
                  #              plot_bgcolor='rgba(0, 0, 0, 0)', 
                   #             paper_bgcolor= 'rgba(0, 0, 0, 0)')

def _complete_fig(fig, title):
        '''Takes a figure and updates the layout and wraps it in html tags'''
        return _wrap_fig(_update_layout(fig), title)

# Variable containg text used in website
texts = json.load(open("text_content.json"))

# Importing and setting theme
external_stylesheets = [dbc.themes.LITERA]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Importing backends
reg_data = Regional_Data()
lo_data  = Location_Data()









##################### Figures #######################

# Create regional data
co_da = reg_data.get_total_cases()

# Total cases by region (bar chart)
total_by_region = px.bar(
        pd.DataFrame({
                "Continent": co_da.index, 
                "Total infected": co_da["new_cases"]
        }), 
        x="Continent", 
        y="Total infected"
)

# Calculate lethality prosentage for each continent (pie chart)
le_pr_cont_pie = px.pie(
        pd.DataFrame({
                "Continent": co_da.index,
                "Lethality": co_da["new_cases"] 
        }),
        names="Continent", 
        values="Lethality"
)





# Create location data
lo_da = lo_data.get_location("Norway")

# Trend data
co_trend = px.line(
        pd.DataFrame({
                "Location": lo_da["date"],
                "Total cases": lo_da["total_cases"]
        }),
        x="Location",
        y="Total cases"
)








# Webpage main layout
app.layout = html.Div(children=[
        dbc.Navbar([
                dbc.Row([
                        dbc.Col(html.H1("Covid-19 data"))
                ])
        ]),

        dbc.Card(dbc.CardBody([
                html.Br(),
                
                dbc.Row([
                        dbc.Col(_complete_fig(total_by_region, "Total cases by continents"), width=7),
                        dbc.Col(_complete_fig(le_pr_cont_pie, "Total cases compared"), width=5)
                ], align='center'),
                
                html.Br(),
                dbc.Row([
                        dbc.Col(_complete_fig(co_trend, "Location"), width=12)
                ], align='center'),

                
                html.Br(),
                dbc.Card(dbc.CardBody([
                        html.P(texts["description"])
                ]))
        ]))
        
])

# Run webpage
if __name__ == '__main__':
        app.run_server(debug=True)