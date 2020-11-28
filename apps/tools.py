import time

import pandas as pd
import numpy as np

'''Various helper methods for different apps'''

def format_array(arr):
        '''Formats the array in array(dict(label: element), dict(label: element)).
        Also capitalizes first letter and replaces underscore with spaces'''
        
        return [{'label': format_col(item), 'value':item} for item in arr]

def format_col(col):
        '''Takes colom values and replaces "_" with " " and capitalises'''
        return col.replace("_", " ").capitalize()
        
# The 3 following functions used for slider convertion:
# https://stackoverflow.com/questions/51063191/date-slider-with-plotly-dash-does-not-work
def toUnix(t):
        '''Converts datetime to unix time'''
        return int(time.mktime(t.timetuple()))

def toDT(unix):
        '''Converts unix time to date'''
        return pd.to_datetime(unix, unit='s').date().strftime("%d/%m/%y")

def format_marks(dTimes):
        '''Formats marks for slider object'''
        unixT = dict()
        for time in dTimes:
                unixT[toUnix(time)] = str(time.strftime('%d-%m-%y'))
        return unixT
        
def get_common(col1, col2):
        '''Takes twp collumns and returns common elemtents'''
        return np.intersect1d(col1, col2)

def format_numbers(num):
        '''Takes a number and converts it to a string and adds commas as thousand separator'''
        return f'{num:,}'

if __name__ == "__main__":
    print(format_numbers(10000000))