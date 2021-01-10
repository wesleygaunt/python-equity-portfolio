
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 14:57:49 2020

@author: Test
"""
import analysis_functions
import general_functions
import pandas as pd
import numpy as np


def momentum(equities, months, start_date, end_date = None):
    
    equities_data_full = equities.get_data(start_date, end_date)    #get all the data
    

    equities_data_interval = general_functions.split_months(equities_data_full,months)
    
    dates_interval = [timestamp.to_pydatetime() for timestamp in equities_data_interval.index]
    momentum_data = pd.DataFrame(index = dates_interval)
    
    momentum_data["int_start"] = dates_interval
    momentum_data["int_end"] = dates_interval
    momentum_data["int_start"] = momentum_data["int_start"].shift(1)
    
    
    percent_data_interval = analysis_functions.percent_change(equities_data_interval,analysis_functions.FROM_PREV_ITEM) 
    
    
    momentum_data["best_prev_equity"]  = percent_data_interval.idxmax(axis = 'columns')
    momentum_data["prev_owned_equity"] = momentum_data["best_prev_equity"].shift(1) #this is based on the previous 

    next_interval_perf = []
    

    prev_perf_slice_final_value = 1
    momentum_percent_data = pd.DataFrame(index = equities_data_full.index)
    
    for date, row in momentum_data.iterrows():
        prev_owned_equity = row["prev_owned_equity"] 
        if (str(prev_owned_equity) != 'nan' and str(prev_owned_equity) != 'NaT'):
            #print("date: " + str(date))
            #print("prev_owned_equity: " + str(prev_owned_equity))
            int_start = row["int_start"].to_pydatetime()
            int_end = row["int_end"].to_pydatetime()           
            int_perf_slice = equities_data_full[prev_owned_equity][int_start:int_end]
            int_perf_slice = prev_perf_slice_final_value * int_perf_slice/int_perf_slice[0] #normalise
            
            
            prev_perf_slice_final_value = int_perf_slice[int_end]
            del int_perf_slice[int_end]
            
            int_perf_slice = pd.DataFrame(int_perf_slice)
            momentum_percent_data[int_start] = int_perf_slice#[prev_owned_equity]  
            equity_col = percent_data_interval[prev_owned_equity]
            current_perf = equity_col.loc[date]# + 1
            
        else:
            momentum_percent_data = momentum_percent_data[date:]
            equities_data_full = equities_data_full[date:]
            current_perf = np.nan
        
        next_interval_perf.append(current_perf)
    
    momentum_data['prev_int_perf'] = next_interval_perf

    percent_data_full = analysis_functions.percent_change(equities_data_full,analysis_functions.FROM_FIRST_ITEM)
    
    percent_data_full = percent_data_full[:int_end]
    percent_data_full['mean'] = percent_data_full.mean(axis = 1)
    equities_data_full = equities_data_full[:int_end]
    momentum_percent_data = momentum_percent_data[:int_end]
    momentum_percent_data[int_start][int_end] = prev_perf_slice_final_value
     
    momentum_percent_data['total'] = momentum_percent_data.sum(axis = 1)
    percent_data_full['momentum'] = momentum_percent_data['total']
    return percent_data_full
        


