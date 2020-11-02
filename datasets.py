# Import pandas for handeling data
import pandas as pd
import json, copy

class Covid_Data(object):
    '''Class can load and operate on covid-19 dataset from ourworld in data
    https://covid.ourworldindata.org/data/owid-covid-data.csv. Class uses a
    json file to load data.'''
    
    paths       = None          # Paths and urls to find datasets
    covid_data  = None          # Covid-19 dataset

    def __init__(self):
        '''Poulates class fields'''
        self.paths          = self._do_load_urls()
        self.covid_data     = self._load_data(self.paths["covid-19"])

    def _load_data(self, paths):
        '''Loads the data from the url array, if it getts an exeption 
        it tries the next one and so on'''
        res = None
        for path in paths:
            try: 
                res = pd.read_csv(path) 
                print("Loaded covid-19 dataset from {}".format(path))
                break
            except Exception as e:
                print("\nError loading dataset\n", e, "\nContinuing anyway...\n")
                continue
        return res

    def _do_load_urls(self, path="dataset_paths.json"):
        '''Loads json file from path parameter'''
        return json.load(open(path))

    def get_grouped_data(self, groups):
        '''Returns pandas groupby object based on groups parameter'''
        return 

    def get_urls(self):
        '''Returns a deepcopy of paths dict'''
        return copy.deepcopy(self.paths)

    def get_summed_cont(self):
        '''Summed data for continent'''
        return self.covid_data.groupby("continent").sum()

    def get_location(self, location):
        '''Get location data'''
        return self.covid_data.groupby("location").get_group(location)

    def get_locations(self):
        '''Returns a column'''
        return self.covid_data["location"].unique()


if __name__ == "__main__":
    cd = Covid_Data()
    