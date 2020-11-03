# Import pandas for handeling data
import pandas as pd
import json, copy

class Data_Handler(object):
    paths       = None          # Paths and urls to find datasets
    covid_data  = None          # Covid-19 dataset

    def __init__(self, url_key, url_path="config/dataset_paths.json"):
        self.paths = self.do_load_urls(url_path)
        self.data = self.load_data(self.paths[url_key])

    def load_data(self, paths):
        '''Loads the data from the url array, if it getts an exeption 
        it tries the next one and so on'''
        res = None
        for path in paths:
            try: 
                res = pd.read_csv(path, parse_dates=True) 
                print("Loaded dataset from {}".format(path))
                break
            except Exception as e:
                print("\nError loading dataset\n", e, "\nContinuing anyway...\n")
                continue
        return res

    def do_load_urls(self, path):
        '''Loads json file from path parameter'''
        return json.load(open(path))

    def get_urls(self):
        '''Returns a deepcopy of paths dict'''
        return copy.deepcopy(self.paths)


class Covid_Data(Data_Handler):
    '''Class can load and operate on covid-19 dataset from ourworld in data
    https://covid.ourworldindata.org/data/owid-covid-data.csv. Class uses a
    json file to load data.'''

    def __init__(self, url_key="covid-19"):
        '''Poulates class fields with the covid dataset'''
        super().__init__(url_key)

    def get_grouped_data(self, groups):
        '''Returns pandas groupby object based on groups parameter'''
        return 

    def get_summed_cont(self):
        '''Summed data for continent'''
        return self.data.groupby("continent").sum()

    def get_location(self, location):
        '''Get location data'''
        return self.data.groupby("location").get_group(location)

    def get_locations(self):
        '''Returns a column'''
        return self.data["location"].unique()

class Tmp_Data(Data_Handler):
    '''Handels temperature data from Kaggle
    https://www.kaggle.com/ksudhir/weather-data-countries-covid19'''

    def __init__(self, url_key="tmp"):
        '''Poulates class fields with temperature data'''
        super().__init__(url_key)

    def get_location(self, location):
        '''Returns the temparture data for a single location'''
        row = self.data[self.data["Country/Region"]==location]

        # Drops the location name set the temperature type as index and transpose
        # which returns a df with parameter as column and date as index
        return row.drop("Country/Region", 1).set_index("weather_param").transpose()

    def get_locations(self):
        '''Returns a column'''
        return self.data["Country/Region"].unique()

if __name__ == "__main__":
    import numpy as np

    cd = Covid_Data()
    td = Tmp_Data()

    cdl = cd.get_locations()
    tdl = td.get_locations()

    cl = np.intersect1d(cdl, tdl)

    print(cl)
    print("td: {}, cd: {}, cl: {}".format(len(cdl), len(tdl), len(cl)))

    print(td.get_location("Norway"))