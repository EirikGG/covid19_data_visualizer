import json, copy

import pandas as pd
import numpy as np

from sklearn.linear_model import Lasso
from scipy.optimize import curve_fit



class Data_Handler(object):
    paths       = None          # Paths and urls to find datasets
    data        = None          # Dataset
    description = None          # Status of dataset e.g. local file or web download

    def __init__(self, url_key, url_path="config/dataset.json"):
        self.paths = self.do_load_urls(url_path)
        self.data, self.description = self.load_data(self.paths[url_key])

    def load_data(self, paths):
        '''Loads the data from the url array, if it getts an exeption 
        it tries the next one and so on'''
        res = None
        for path_obj in paths:
            path = path_obj["path"]
            try: 
                res = pd.read_csv(path, parse_dates=True)
                des = path_obj["description"]
                print("Loaded dataset from {}".format(path))
                break
            except Exception as e:
                print("\nError loading dataset\n", e, "\nContinuing anyway...\n")
                continue
        return res, des

    def do_load_urls(self, path):
        '''Loads json file from path parameter'''
        return json.load(open(path))["paths"]

    def get_urls(self):
        '''Returns a deepcopy of paths dict'''
        return copy.deepcopy(self.paths)

    def get_description(self):
        '''Returns the description of data set, eg. local file or web download'''
        return self.description

    def get_data(self):
        '''Returns a copy of the pandas dataframe containing the dataset'''
        return copy.deepcopy(self.data)

class Covid_Data(Data_Handler):
    '''Class can load and operate on covid-19 dataset from ourworld in data
    https://covid.ourworldindata.org/data/owid-covid-data.csv. Class uses a
    json file to load data.'''

    def __init__(self, url_key="covid-19"):
        '''Poulates class fields with the covid dataset'''
        super().__init__(url_key)
        self.data["date"] = pd.to_datetime(self.data["date"])


    def get_summed_cont(self):
        '''Summed data for continent'''
        return self.data.groupby("continent").sum()

    def get_location(self, location):
        '''Get location data'''
        return self.data.groupby("location").get_group(location)

    def get_locations(self):
        '''Returns a available locations, uses :-2 to remove international and world'''
        return self.get_col("location").unique()[:-2]

    def get_dates(self):
        '''Returns date column as datetime objects'''
        return pd.to_datetime(self.get_col("date"))

    def get_col(self, col):
        '''Returns a column'''
        return self.data[col]

    def get_cols(self):
        '''Returns all columns'''
        return self.data.columns

    def get_date(self, date):
        '''Returns data from one spesific date'''
        return self.data[date==self.data["date"]]

    def get_total_by_iso(self):
        '''Filters data and returns total cases and iso codes'''
        data_filtered = self.data[(self.data["location"] != "World") &
                                (self.data["location"] != "International")]
        return data_filtered.groupby(["iso_code", "location"])["total_deaths"].max("date")

    def get_iso(self, iso):
        '''Getts dataframe for spesific iso code'''
        return self.data[iso == self.data["iso_code"]]

    def get_loc_from_iso(self, iso):
        '''Returns full location name from iso code based on dataset'''
        return self.get_iso(iso)["location"].values[0]

    def get_feature_ranking(self, feature):
        with open("config/dataset.json", "r") as f:
                features = json.load(f)["regression"]["features"]

        features.remove(feature)
        
        data_dropna = self.data.fillna(0)

        lasso_model = Lasso(alpha=.1, normalize=True, max_iter=100000, positive=True)
        lasso_model.fit(data_dropna[features], data_dropna[feature])

        df = pd.DataFrame(dict(features=features, coeff=lasso_model.coef_.round(2))).sort_values("coeff", ascending=False)
        return df[0 != df["coeff"]]

    def get_tot_pr_m_cont(self):
        '''Return data per million for continents'''
        return self.data.groupby(["continent", "location"]).max("date").sum(level="continent")

    def get_cont(self, cont):
        '''Filters data and returns data for each continent'''
        return self.data.groupby(["continent", "date"]).sum().xs(cont, level="continent")

    def get_conts(self):
        '''Returns all continents'''
        return self.data["continent"].dropna().unique()

    def add_tmp(self, name, tmp_func):
        locs = self.data["location"].unique()
        avgs = pd.DataFrame(dict(tmp=[tmp_func(loc) for loc in locs]), index=locs)

        self.data[name] = self.data["location"]
        self.data[name] = self.data[name].apply(lambda x: avgs.loc[x].values[0])

        return self.data

    def get_pred(self, loc, col, days=1):
        '''Returns extrapolated predictions for a single location'''
        loc_data = self.data[loc == self.data["location"]].sort_values("date", ascending=True)

        date_ind = pd.DataFrame(
            dict(total_cases=loc_data["total_cases"].values),
            index=loc_data["date"]
        )

        date_ind_ex = date_ind.reindex(date_ind.index.append(date_ind.index + pd.DateOffset(days=days)))
        date_ind_ex = date_ind_ex.fillna(0)

        tmp_date = date_ind_ex.index
        date_ind_ex = date_ind_ex.reset_index()
        
        x = date_ind_ex.index.astype(float).values
        y = date_ind_ex["total_cases"].values

        def func(x, a, b, c, d):
            return a * (x ** 3) + b * (x ** 2) + c * x + d

        params = curve_fit(
            func,
            x,
            y
        )

        x = date_ind_ex[pd.isnull(date_ind_ex["total_cases"])].index.astype(float).values
        date_ind_ex["total_cases"][x] = func(x, params["total_cases"])

        date_ind_ex.index = tmp_date
        return date_ind_ex

    def get_filtered_data_loc(self, col, operator, value):
        '''Filters data and returns locations'''
        data = None
        if "equals" == operator:
            data = self.data[value == self.data[col]]
        elif "greater" == operator:
            data = self.data[value <= self.data[col]]
        elif "less" == operator:
            data = self.data[value >= self.data[col]]

        return data["location"].unique()
        
        
class Tmp_Data(Data_Handler):
    '''Handels temperature data from Kaggle
    https://www.kaggle.com/ksudhir/weather-data-countries-covid19'''

    def __init__(self, url_key="tmp"):
        '''Poulates class fields with temperature data'''
        super().__init__(url_key)
        
    def get_location(self, location):
        '''Returns the temparture data for a single location'''
        row = self.data[self.data["Country/Region"]==location]      # Sort one location
        row = row.drop("Country/Region", 1)                         # Drops location column
        row = row.set_index("weather_param").transpose()            # Set index to date and transposes
        row.index = pd.to_datetime(row.index)                       # Parse index to datetime format
        return row

    def get_locations(self):
        '''Returns a column'''
        return self.data["Country/Region"].unique()
    
    def get_loc_group(self):
        avg = pd.DataFrame(columns=self.data.columns[2:], index=self.get_locations())            # New dataframe with average tmp for each country
        group_loc = self.data.groupby("Country/Region")
        for country in avg.index:
            group = group_loc.get_group(country)

            maxT = group[group["weather_param"]=="maxtempC"].drop(["Country/Region", "weather_param"], 1)
            minT = group[group["weather_param"]=="mintempC"].drop(["Country/Region", "weather_param"], 1)
            
            avg.loc[country] = (maxT.values + minT.values) / 2
        
        avg = avg.transpose()

        avg.index = pd.to_datetime(avg.index)
            
        return avg

    def get_avg(self, loc):
        '''Returns average temperature for location'''
        w_dat = self.get_location(loc)
        if not w_dat.empty:
            w_dat["avg"] = (w_dat["maxtempC"] + w_dat["mintempC"]) / 2
            return w_dat["avg"].mean()
        else:
            return np.NaN

if __name__ == "__main__":
    c = Covid_Data()
    t = Tmp_Data()
    
    pred = c.get_pred("Norway", "total_cases")
    
    print(pred.head())
    print(pred.tail())
    '''
    test = pd.DataFrame(dict(x1 = [1, 2, 3], x2 = [4, 5, 6]), index = pd.to_datetime(["27-11-2013", "28-11-2013", "29-11-2013"]))
    print(test)
    test = test.reindex(test.index.append(test.index + pd.DateOffset(days=3)))
    print(test)
    '''