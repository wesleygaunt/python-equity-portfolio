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
import transaction_history

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
    def __init__(self, equities, start_date, end_date, duration_months):
        portfolio = Portfolio()
        
        self.equities = equities
        self.start_date = start_date
        
        self.end_date = end_date
        self.duration_months = duration_months
        self.transaction_history = transaction_history.TransactionHistory()

        
    def run(self):

        current_date = self.start_date
        #0 initial portfolio
        
        while(current_date < self.end_date):
            #1 buy 
            
            #peform single rule on all possible holdings
           
            growth_last_6_months = equity_growth(self.equities, current_date,self.duration_months)

            best_equity_name = growth_last_6_months.idxmax()
            best_equity_performance = growth_last_6_months[best_equity_name]
            best_equity = self.equities[best_equity_name]
            print(str(current_date.date()) 
                  + ", best performing equity in " 
                  + str(self.duration_months) + " months: "
                  + best_equity_name
                  + " with "
                  + str(best_equity_performance))
            
            #buy which one meets rule
            self.transaction_history.buy_equity(best_equity, current_date,method = BY_VAL)

            
            
            
            # 2 wait duration
            current_date = current_date + relativedelta(months=+self.duration_months)
            
            # 3 sell
                #peform single rule on all current holdings
                
                #sell which one meets rule
                
        
    
#growth_1 = equity_growth(data.legg_mason_japan, current_date ,duration_months)
        
start_date = datetime.datetime(2013,1,1) 
end_date = datetime.datetime(2021,1,1) 

growth_2 = equity_growth(data.funds, start_date,duration_months)


# while(current_date < end_date):
#     growth_last_6_months = equity_growth(data.funds, current_date,duration_months)

#     best_equity_name = growth_last_6_months.idxmax()
#     print(str(current_date.date()) +" : " + best_equity_name)
    
#     current_date = current_date + relativedelta(months=+duration_months)

algorithm = Algorithm(data.funds, start_date, end_date, duration_months)
algorithm.run()

