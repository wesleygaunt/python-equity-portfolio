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



def percent_change_from_beginning(input_data):        
    return percent_change(input_data,FROM_FIRST_ITEM)
    
def percent_change_from_prev_item(input_data):
    return percent_change(input_data,FROM_PREV_ITEM)
    
    
def percent_change(input_data, method = FROM_FIRST_ITEM):
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
            
            else:
                return
            
            percent_change = pd.DataFrame(percent_change)
            
            percent_data[name] = percent_change + 1
    
    
    return percent_data
    

  
    