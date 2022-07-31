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

#do not upload to GitHub
#from ft_data_request import ft_data_request
#from morningstar_data_request import morningstar_data_request
   

#INTERVAL_WEEK = 'week'
#INTERVAL_DAY = 'day'
#TIMEDELTA_DAY = datetime.timedelta(days = 1)
#TIMEDELTA_WEEK = datetime.timedelta(weeks = 1)

def morningstar_data_request(provider_code, start_date, end_date):
    url = "https://tools.morningstar.co.uk/api/rest.svc/timeseries_cumulativereturn/t92wz0sj7c?currencyId=GBP&idtype=Morningstar&frequency=daily&startDate=1970-01-01&performanceType=&outputType=COMPACTJSON&id=F0000150IV]2]0]FOGBR$$ALL&decPlaces=8&applyTrackRecordExtension=true"

    return

def yahoo_request(provider_code,start_date, end_date):
    """
    Gets end of day data from yahoo finance for a equity or fund.
    
    usage:
    yahoo_request('0P00000VC9.L',datetime.datetime(2019,1,1),datetime.datetime(2020,1,1))
    

    Parameters
    ----------
    provider_code : str
        The code that is passed to the 
        
        ie for https://uk.finance.yahoo.com/quote/0P00000VC9.L?p=0P00000VC9.L
        the provider code is '0P00000VC9.L'
        
        
    unit : str
        'GBp' or 'GBP' get from page on yahoo
    start_date : datetime.datetime
        The data start date.
    end_date : datetime.datetime
        The data end date..

    Returns
    -------
    pandas.DataFrame
        A dataframe with datetime index and price.

    """
    #save for later
    initial_start_date = start_date
    initial_end_date = end_date
    end_date = min(end_date,datetime.datetime.now())


    if((end_date == None) or (end_date == start_date)):   #if no end date was supplied, set the end_date to the start_date. This will now request a single day.
        initial_end_date = initial_start_date
        end_date = start_date

    try:
        start_date = start_date - datetime.timedelta(weeks = 1)     #in case the data is not available
    except:
        start_date = start_date
    
    
    
    start_date_unix = general_functions.unix_date(start_date)
    end_date_unix = general_functions.unix_date(end_date + datetime.timedelta(days = 1))    #yahoo request is not inclusive of the end date, so add a single day (in seconds) onto the 
        
    url = "https://query1.finance.yahoo.com/v7/finance/download/"+provider_code+"?"+"period1="+ str(start_date_unix) + "&period2=" + str(end_date_unix) + "&interval=1d&events=history"
    #https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
    try:
        r = requests.get(url,allow_redirects = True)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("HTTPError: " + str(err))
        return None   #s
        #raise SystemExit(err)
    
    data_string = r.content.decode("utf-8")
    
    data_io = StringIO(data_string)     #https://stackoverflow.com/questions/22604564/create-pandas-dataframe-from-a-string
    df = pd.read_table(data_io,sep = ',')       
    
    #convert to time series https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html    
    dates = pd.to_datetime(df['Date'])
    df.index = dates
    df.drop('Date',1,inplace = True) #same as del df['Date']
    
    #drop blank rows:https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html
    df.dropna(how = 'all',inplace = True)
    
    df = df['Close']    #only select close row
    
    df = df.to_frame()
    
    df.columns = ['Price']
    
    #convert to GBP (£)?
     
    df = df.sort_index()
    

    earliest_date = min(df.index)
    if(earliest_date > initial_start_date):
        df = df[initial_start_date:initial_end_date]
        return df
    else:
        data_upto_and_including_start = df[earliest_date:initial_start_date]
        data_start = pd.DataFrame(data_upto_and_including_start.iloc[-1]).T #get the earliest date before the initial
        
    
        df = df[initial_start_date:initial_end_date]
    
        if(initial_start_date not in df.index):
            df = df.append(data_start)
            df = df.sort_index()
        
        
    
        return df


def investing_com_csv_request(provider_code,start_date, end_date):
    """
    This function exracts the data from a csv file that has been downloaded from investing.com

    Parameters
    ----------
    provider_code : TYPE
        DESCRIPTION.
    unit : TYPE
        DESCRIPTION.
    start_date : TYPE
        DESCRIPTION.
    end_date : TYPE
        DESCRIPTION.
    interval : TYPE, optional
        DESCRIPTION. The default is INTERVAL_DAY.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    
    initial_start_date = start_date
    initial_end_date = end_date

    file = 'data\\'+ provider_code + ' Historical Data.csv'
    try:
        df = pd.read_table(file,sep = ',')

    except:
        warnings.warn(file + " not found",category = UserWarning,stacklevel=4)
        return None

    
    dates = pd.to_datetime(df['Date'])
    df.index = dates
    df.drop('Date',1,inplace = True) #same as del df['Date']

    df.dropna(how = 'all',inplace = True)

    df = df['Price']
    df = df.to_frame()
    
    df = df.sort_index()

    earliest_date = min(df.index)
    if(earliest_date > initial_start_date):
        df = df[initial_start_date:initial_end_date]
        return df
    else:
        data_upto_and_including_start = df[earliest_date:initial_start_date]
        data_start = pd.DataFrame(data_upto_and_including_start.iloc[-1]).T #get the earliest date before the initial
        
    
        df = df[initial_start_date:initial_end_date]
    
        if(initial_start_date not in df.index):
            df = df.append(data_start)
            df = df.sort_index()
    
    
    return df


#store the functions in a dictionary, in a functional manner
request_functions = {'yahoo':yahoo_request,'investing_com_csv':investing_com_csv_request,'ft': ft_data_request,'morningstar':morningstar_data_request}
   
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