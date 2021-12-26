# -*- coding: utf-8 -*-
"""
A collection of general use functions.
"""
import datetime
import calendar
import pandas
from collections import abc


def unix_date(date):   
    """
    Converts a datetime into a unix date

    Parameters
    ----------
    date : datetime.datetime
        A datetime to convert.

    Returns
    -------
    unix : int
        The date in unix format (seconds from the epoch).

    """
    #date = datetime.datetime(year, month, day)
    epoch = datetime.datetime(1970,1,1)

    unix = int((date - epoch).total_seconds())          #https://stackoverflow.com/questions/19801727/convert-datetime-to-unix-timestamp-and-convert-it-back-in-python
    
    return unix


def to_spaces(input_string):
    """
    Converts underscroes (_) and hyphens (-) in a string to spaces

    Parameters
    ----------
    input_string : str
        Input string.

    Returns
    -------
    output_string : str
        Output string.

    """
    input_string = str(input_string)
    output_string = input_string.replace("_"," ").replace("-", " ")
    return output_string

def capitalize_and_underscore(input_string):
    """
    Converts a string to CAPITALS and replaces all spaces and hypens to underscores.

    Parameters
    ----------
    input_string : str
        Input string.

    Returns
    -------
    output_string : str
        Output string.

    """
    input_string = str(input_string)
    output_string = input_string.replace(" ","_").replace("-", "_").upper()
    output_string = remove_duplicate_chars(output_string)
    return output_string

def remove_duplicate_chars(input_string):
    """
    Removes double underscores (spaces) from strings.

    Parameters
    ----------
    input_string : TYPE
        DESCRIPTION.

    Returns
    -------
    output_string : TYPE
        DESCRIPTION.

    """
    prev_char = ''
    output_string = ''
    for char in input_string:
        if(char == prev_char == '_'):
            continue
        else:
            output_string = output_string + char
            prev_char = char
    return output_string


def convert_to_ISIN(input_string):
    """
    Raises a warning if the input string is not a valid ISIN.

    Parameters
    ----------
    input_string : str
        Input string.

    Returns
    -------
    output_string : str
        Output string.

    """
    #https://www.isin.org/isin/
    #Used for converting ISINs into the right format
    input_string = str(input_string)
    output_string = input_string.replace("-","").replace("_", "").upper()
    # if(len(output_string) != 12):
    #     warnings.warn(output_string + " is not a valid ISIN",category = UserWarning,stacklevel=3)
    return output_string 
    
def previous_weekday(date):
    """
    If the date is a sat or sun, return the previous friday. else return the same day


    Parameters
    ----------
    date : datetime.datetime
        Input date.

    Returns
    -------
    date : datetime.datetime
        Output date, will be a friday if the input date is a weekend.

    """
    if (date.isoweekday() == 6): #if sat
        td = datetime.timedelta(days = 1)
        date = date - td
        return date
    elif (date.isoweekday() == 7): #if sun
        td = datetime.timedelta(days = 2)
        date = date - td
        return date
    else:
        return date
    


def add_months(sourcedate, months):
    """
    Add a number of months to a date

    Parameters
    ----------
    sourcedate : datetime.datetime
        Iput date.
    months : int
        Number of months to add.

    Returns
    -------
    datetime.datetime
        Output date.

    """
    #https://stackoverflow.com/questions/4130922/how-to-increment-datetime-by-custom-months-in-python-without-using-library
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.datetime(year, month, day)




def nearest(items, pivot):
    """
    Returns nearest item to 'pivot' that appears in a list of items. Is used to find the nearest date in a datetime_index
        
    #https://stackoverflow.com/questions/32237862/find-the-closest-date-to-a-given-date


    Parameters
    ----------
    items : TYPE
        DESCRIPTION.
    pivot : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if pivot in items:
        return pivot
    else:
        return min(items, key=lambda x: abs(x - pivot))

def nearest_before(items, pivot):
    """
    Returns the nearest item in a list that is before the pivot.

    Parameters
    ----------
    items : TYPE
        DESCRIPTION.
    pivot : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    items_before = [item for item in items if item<=pivot]
    
    if(items_before != []):
        return max(items_before)
    else:
        return None

def nearest_after(items, pivot):
    """
    Returns the nearest item in a list that is after the pivot.


    Parameters
    ----------
    items : TYPE
        DESCRIPTION.
    pivot : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    items_after = [item for item in items if item>=pivot]
    
    if(items_after != []):
        return min(items_after)
    else:
        return None

def split_months(data_full, months):
    """
    Splits the data by a specfied no of months, discard the rest. Will attempt to find the closest date that appears in the data_full (ie if the expected date is not available)

    Parameters
    ----------
    data_full : pd.DataFrame with DateTime index.
        Full input data.
    months : int
        DESCRIPTION.

    Returns
    -------
    data_interval : pandas.DataFrame
        DESCRIPTION.

    """
    dates_full = data_full.index
    
    #dates_interval will contain a list of the dates seperated by the no months spec in months
    dates_interval = []
    
    start_date = dates_full[0].to_pydatetime() #may not be = to start date
    end_date = dates_full[-1]
    
    date = start_date
    while(date<=end_date):
        dates_interval.append(nearest(dates_full,date)) #this will look for the dates_interval in the index that are closest to the ones specified 6_mths apart
        date = add_months(date,months)
        date = datetime.datetime(date.year, date.month, date.day)

    #dates_interval = [timestamp.to_pydatetime() for timestamp in dates_interval] #convert to datetime

    data_interval = data_full.loc[dates_interval] #get split data
    return data_interval#,dates_interval

def get_collection_items(collection):
    #return the items in dict form - with the indexes as the keys for non-mapping types
    if(isinstance(collection, abc.Mapping)): 
        items =  collection
            
    elif(isinstance(collection, abc.Sequence)): 
        #lists and tuples
        item_keys = range(0,len(collection))
        items = {str(item_key) : collection[item_key] for item_key in item_keys}
    elif(isinstance(collection,abc.Set)):
        #sets
        item_keys = range(0,len(collection))
        zip_items = zip(item_keys,collection)
        items = {str(item_key) : item for item_key, item in zip_items}
    else:
        print("unknown collection type")
        return
    return items

def QDate_to_datetime(_Qdate):
    """
    Converts a Qt QDate format to a python datetime.

    Parameters
    ----------
    _Qdate : QDate
        DESCRIPTION.

    Returns
    -------
    date : datetime
        DESCRIPTION.

    """
    date = datetime.datetime(year = _Qdate.year(), month = _Qdate.month(), day = _Qdate.day())
    return date

def ensure_datetime_index(data):
    """
    Returns a dataFrame or series with the correct orientation

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.

    Returns
    -------
    data : TYPE
        DESCRIPTION.

    """
    if(type(data) == pandas.DataFrame or type(data) == pandas.Series):
        if(type(data.index) == pandas.core.indexes.datetimes.DatetimeIndex and type(data.columns) != pandas.core.indexes.datetimes.DatetimeIndex):
            #all good, already correct orientation
            return data
        elif(type(data.index) != pandas.core.indexes.datetimes.DatetimeIndex and type(data.columns) == pandas.core.indexes.datetimes.DatetimeIndex):
            #wrong orientation    
            data = data.T
            return data
        else:
            return data
    else:
        return data