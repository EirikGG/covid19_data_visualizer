# Import pandas for handeling data
import pandas as pd
import json, copy

class Data_Handler():
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
        return self.covid_data.groupby(groups)

    def get_urls(self):
        '''Returns a deepcopy of paths dict'''
        return copy.deepcopy(self.paths)

class Regional_Data(Data_Handler):
    '''Sorts data into regions'''
    reg_data = None                 # Holds dataset sorted into regions as groupby object

    def __init__(self):
        super().__init__()
        self.reg_data = super().get_grouped_data(("continent"))

    def get_total_cases(self):
        return self.reg_data.sum()

class Location_Data(Data_Handler):
    '''Sorts data into location'''
    loc_data = None                 # Holds dataset sorted into locations as groupby object

    def __init__(self):
        super().__init__()
        self.loc_data = super().get_grouped_data(("location"))

    def get_location(self, location):
        return self.loc_data.get_group(location)
        
if __name__ == "__main__":
    ld = Location_Data()
    print(ld.get_summed("Norway"))