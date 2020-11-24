import dash, json, time
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from sklearn import preprocessing

from datasets import Covid_Data, Tmp_Data



# Variable containg text used in website
texts = json.load(open("config/text_content.json"))

# Importing and setting theme
external_stylesheets = [dbc.themes.SIMPLEX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

server = app.server

# Importing backends
co_da = Covid_Data()    # Covid data
t_da = Tmp_Data()       # Temperature data                






















