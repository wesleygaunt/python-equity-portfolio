# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 19:06:04 2020

@author: Test
"""
import pandas as pd
import general_functions
from datetime import datetime
FROM_FIRST_ITEM = 'first'
FROM_PREV_ITEM = 'prev'
FROM_DATE = 'date'



def percent_change_from_beginning(input_data):        
    return percent_change(input_data,FROM_FIRST_ITEM)
    
def percent_change_from_prev_item(input_data):
    return percent_change(input_data,FROM_PREV_ITEM)
    
    
def percent_change(input_data, method = FROM_FIRST_ITEM, date = None):
    """
    Calculates the percent change of a series or dataframe. 

    Parameters
    ----------
    input_data : pandas.Series or pandas.DataFrame
        Input data to process
    method : str
        'first' or analysis_functions.FROM_FIRST_ITEM
         'prev' or analysis_functions.FROM_PREV_ITEM 
         default: 'first'
         Method in which to calculate the percentage change.

    Returns
    -------
    percent_data : pandas.DataFrame
        DataFrame containing the percentage change data. This is given as a ratio of the old value, ie if the value has increased by 20%, the output will be 1.2

    """

    if type(input_data) == pd.DataFrame:
        if(input_data.empty):
            return input_data
        input_data.fillna(method = 'ffill',inplace = True)
        percent_data = pd.DataFrame()
        percent_data = input_data.copy()
        
        for name in input_data:
        
            col = input_data[name]
            col.dropna(inplace = True)
            
            if(method == FROM_FIRST_ITEM):
                start_val = col.iloc[0]
                change = col - start_val
                percent_change = change/start_val
            
            elif(method == FROM_PREV_ITEM):
                percent_change = col.pct_change()
                
            elif(method == FROM_DATE):
                if(date == None):   #same as FROM_FIRST_ITEM
                     start_val = col.iloc[0]
                else:
                    nearest_date = general_functions.nearest(list(input_data.index),date)
                    start_val = col.loc[nearest_date]
                change = col - start_val
                percent_change = change/start_val
            
            else:
                return
            
            percent_change = pd.DataFrame(percent_change)
            
            percent_data[name] = percent_change + 1
    
    
    return percent_data


def annual_performance(input_data):
    """
    Calculates the annual performance of the data

    Returns
    -------
    data_split_percentage : TYPE
        DESCRIPTION.

    """        
    input_data = input_data.copy()
    
    start_year = input_data.index[0].year #may not be = to start date
    end_year = input_data.index[-1].year #may not be = to start date

    start_new_year = datetime(start_year + 1,1,1)
    end_new_year = datetime(end_year,1,1)
    

    input_data = input_data[start_new_year:end_new_year]
    data_split = general_functions.split_months(input_data, 12)
    data_split_percentage = percent_change_from_prev_item(data_split) - 1
    
    year_list = [date.year - 1 for date in data_split_percentage.index]
    data_split_percentage.index = year_list
    
    return data_split_percentage


  
    