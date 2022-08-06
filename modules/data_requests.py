# -*- coding: utf-8 -*-
"""
Requests data from internet from one of four data services. Yahoo and investing.com are shown, but ft and morningstar are in different files.
"""
import datetime
import warnings
import pandas as pd
from io import StringIO
import requests
import general_functions
import constants

#do not upload to GitHub
#from ft_data_request import ft_data_request
#from morningstar_data_request import morningstar_data_request
   

#INTERVAL_WEEK = 'week'
#INTERVAL_DAY = 'day'
#TIMEDELTA_DAY = datetime.timedelta(days = 1)
#TIMEDELTA_WEEK = datetime.timedelta(weeks = 1)

def request_morningstar_data(provider_code, start_date = None, end_date = None):
    
    url = ("https://tools.morningstar.co.uk/api/rest.svc/"
    #+ "timeseries_cumulativereturn/"
    + "timeseries_price/"
    + "t92wz0sj7c?"
    + "currencyId=GBP"
    + "&idtype=Morningstar"
    + "&frequency=daily"
    + "&performanceType="
    + "&outputType=COMPACTJSON"
    + "&id=" + provider_code
    #+ "]2]0]FOGBR$$ALL"
    + "&decPlaces=8"
    + "&applyTrackRecordExtension=true")
    
    if(start_date == None):
        start_date = constants.MIN_DATE
        
    try:
        #if datetime format
        start_date_iso = start_date.date().isoformat()
    except:
        #if date format
        start_date_iso = start_date.isoformat()
        
    url += "&startDate=" + start_date_iso
        
    if(end_date != None):
        try:
            #if datetime format
            end_date_iso = end_date.date().isoformat()
        except:
            #if date format
            end_date_iso = end_date.isoformat()
        url = url + "&endDate=" + end_date_iso
    
    df = pd.read_json(url)
    df.columns = ['Date', 'Price']
    df['Date'] = pd.to_datetime(df['Date'], unit = 'ms')
    df.index = pd.DatetimeIndex(df['Date'])
    del df['Date']
    return df


#store the functions in a dictionary, in a functional manner
#
request_functions = {'morningstar':request_morningstar_data}
   
def request_hist_data(provider, provider_code, unit, start_date, end_date = None):
    """
    

    Parameters
    ----------
    provider : str
        'yahoo','investing_com_csv','ft','morningstar'
    provider_code : TYPE
        DESCRIPTION.
    unit : TYPE
        DESCRIPTION.
    start_date : TYPE
        DESCRIPTION.
    end_date : TYPE, optional
        DESCRIPTION. The default is None.

    Raises
    ------
    an
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """


    #need to get the correct function
    try:
        request_function = request_functions[provider]
    except KeyError:
        print("KeyError: provider \"" + str(provider) + "\" does not exist")
        return None
    
    df = request_function(provider_code,  start_date,end_date)  #this might internally raise an error, but it will be printed and then suppressed.

    if(df is None):
        return None
        
    
    #if the data comes in GBp, need to turn it to GBP!
    if(unit == 'GBp'):
        print("GBp")
        df = df/100;    
            
    df = df.sort_index()
    
    df = __unit_change_check(df)
    return df
    

def __unit_change_check(input_data):
    """
    This function checks if there is a large jump in the data that could indicate a data unit change (ie GBP to GBp or vice versa). 
    It raises a warning and changes the data to the range that it was quoted to at the end.
    ie if the function has the following values, which indicate a change from GBP to GBp
        1.011, 1.028, 103.4 104.2
        it will return 101.1 102.8 103.4 104.2

    Parameters
    ----------
    input_data : pandas.DataFrame
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    if(input_data.size <= 1):
        return input_data
    
    min_threshold_jump_up = 100*(100 - 10)
    max_threshold_jump_up = 100*(100 + 10)
    threshold_jump_down = -1 * (100 - 10)
    
    name = input_data.columns[0]
    
    
    percent_change = 100*input_data.pct_change()
    percent_change.dropna(how = 'all',inplace = True)

    max_change = max(percent_change[name])
    min_change = min(percent_change[name])
    max_index = percent_change.idxmax()[0].to_pydatetime()
    min_index = percent_change.idxmin()[0].to_pydatetime()

    if((min_threshold_jump_up < max_change) and (max_change < max_threshold_jump_up)):
        warnings.warn("The price changed by: " + str(max_change) + " % (" + str(max_change/100)  + " x ) this is probably a unit change",category = UserWarning,stacklevel=4)
        new_unit_vals = input_data[max_index:]
        
        old_unit_vals = input_data[:max_index]
    
        old_unit_vals = old_unit_vals.drop(max_index)
        old_unit_vals = 100 * old_unit_vals
        
        new_data = old_unit_vals.append(new_unit_vals)
        new_data = new_data.sort_index()        
        
        return new_data

    if(min_change < threshold_jump_down):
        warnings.warn("The price changed by: " + str(min_change) + " % (" + str(min_change/100)  + " x ) this is probably a unit change",category = UserWarning,stacklevel=4)

        new_unit_vals = input_data[min_index:]
        
        old_unit_vals = input_data[:min_index]
    
        old_unit_vals = old_unit_vals.drop(min_index)
        old_unit_vals = old_unit_vals/100
        
        new_data = old_unit_vals.append(new_unit_vals)
        new_data = new_data.sort_index() 
        
        
        return new_data
    
    return input_data