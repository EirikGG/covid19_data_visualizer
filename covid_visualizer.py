import dash, json
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from covid_data import Regional_Data

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

# Variable containg text used in website
texts = json.load(open("text_content.json"))

# Importing and setting theme
external_stylesheets = [dbc.themes.SLATE]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Importing backend
reg_data = Regional_Data()









##################### Figures #######################

# Create regional data figures
co_da = reg_data.get_total_cases()

# Total cases by region (bar chart)
total_by_region = px.bar(pd.DataFrame({
                "Continent": co_da.index,
                "Total infected": co_da["new_cases"]}), 
        x="Continent", 
        y="Total infected").update_layout(template='plotly_dark', 
                                        plot_bgcolor='rgba(0, 0, 0, 0)', 
                                        paper_bgcolor= 'rgba(0, 0, 0, 0)')

# Calculate lethality prosentage for each continent (pie chart)
le_pr_cont_pie = px.pie(pd.DataFrame({
                "Continent": co_da.index,
                "Lethality": co_da["new_cases"]}), 
        names="Continent", 
        values="Lethality").update_layout(template='plotly_dark', 
                                        plot_bgcolor='rgba(0, 0, 0, 0)', 
                                        paper_bgcolor= 'rgba(0, 0, 0, 0)')










# Webpage main layout
app.layout = html.Div(children=[
        dbc.Card(dbc.CardBody([
                html.H1(children='COVID-19 data'), 
                html.Br(),
                
                dbc.Row([
                        dbc.Col(_wrap_fig(total_by_region, "Total cases by continents"), width=7),
                        dbc.Col(_wrap_fig(le_pr_cont_pie, "Total cases compared"), width=5)
                ], align='center'),

                
                html.Br(),
                dbc.Card(dbc.CardBody([
                        html.H5(texts["description"])
                ]))
        ]))
        
])

# Run webpage
if __name__ == '__main__':
        app.run_server(debug=True)
