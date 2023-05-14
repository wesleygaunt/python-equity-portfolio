#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 16:54:45 2023

@author: wes
"""
from portfolio import Portfolio
import datetime 
from dateutil.relativedelta import relativedelta
import data 
import general_functions
import analysis_functions
from time import process_time
import equity 
import pandas

current_date = datetime.datetime(2023,1,1) 

duration_months = 6

start_date = current_date - relativedelta(months=+duration_months)


equity_dict = equity.EquityDict()

equity_dict.add([data.jupiter_uk_smaller_companies,data.legg_mason_japan])

# def equity_growth(equity, current_date, duration_months):
#     start_date = current_date - relativedelta(months=+duration_months)
#     #print(start_date)
#     data = equity.get_data(start_date, current_date)
#     #print(data)
#     growth = analysis_functions.percent_change_from_beginning(data)
#     #print(growth)
#     #print(equity.name)
#     return growth[equity.name][-1]


def equity_growth(equity_input, current_date, duration_months):
    if(type(equity_input) == equity.EquityDict):
        #t1 = process_time()
        #growth = {equity_name: equity_growth(equity_input[equity_name], current_date, duration_months) for equity_name in equity_input}
        
        #t2 = process_time()
        start_date = current_date - relativedelta(months=+duration_months)
        data = equity_input.get_data(start_date, current_date)
        #growth = pandas.DataFrame(data.iloc[0] / data.iloc[-1]).T
       # t3 = process_time()
        
        # print(t2 - t1)
        # print(t3 - t2)
        growth = data.iloc[0] / data.iloc[-1]

        return growth
    else:
    
        start_date = current_date - relativedelta(months=+duration_months)
        data = equity_input.get_data(start_date, current_date)
     
        
        val1 = data[equity_input.name][0] #first val
        val2 = data[equity_input.name][-1] #second val
        growth= val2/val1
    
        return growth
    
class Algorithm:
    def __init__(self, equities):
       portfolio = Portfolio() 


growth_1 = equity_growth(data.legg_mason_japan, current_date ,duration_months)
growth_2 = equity_growth(data.funds, current_date,duration_months)


# 0 initial portfolio
# 1 wait duration
# 2 sell
    #peform single rule on all current holdings
    #sell which one meets rule
# 3 buy 
        #peform single rule on all possible holdings
        #sell which one meets rule
        
current_date = datetime.datetime(2013,1,1) 
end_date = datetime.datetime(2021,1,1) 


while(current_date < end_date):
    growth_last_6_months = equity_growth(data.funds, current_date,duration_months)

    best_equity_name = growth_last_6_months.idxmax()
    print(str(current_date) +" : " + best_equity_name)
    
    current_date = current_date + relativedelta(months=+duration_months)