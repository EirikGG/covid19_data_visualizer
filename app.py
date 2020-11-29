import dash, json, time
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from sklearn import preprocessing

from datasets.datasets import Covid_Data, Tmp_Data, Travel_Data



# Variable containg text used in website
texts = json.load(open("config/text_content.json"))

# Importing and setting theme
external_stylesheets = [dbc.themes.SIMPLEX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, 
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])


# Importing backends
co_da = Covid_Data()    # Covid data
t_da = Tmp_Data()       # Temperature data
tr_da = Travel_Data()   # Travel data