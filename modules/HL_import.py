# -*- coding: utf-8 -*-
"""
Creates a transaction history object from a Hargreaves Lansdown csv transaction history file.
"""
import pandas as pd
from datetime import datetime
from transaction_history import TransactionHistory
import general_functions

def string_date_to_datetime(date):
    date = date.split('/')
    date = datetime(year = int(date[2]),month = int(date[1]), day = int(date[0]))
    return date
    
def HL_import(filename,equities, initial_import = False):
    """
    Imports a Hargreaves Lansdown portfolio history into a transaction_history 
    object.

    Parameters
    ----------
    filename : TYPE
        DESCRIPTION.
    equities : TYPE
        DESCRIPTION.
    initial_import : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """

    HL_raw = pd.read_csv(filename)#,encoding = 'unicode_escape')
    equities_list = []

    trade_date = HL_raw['Trade date']
    trade_date = [string_date_to_datetime(date) for date in trade_date]
    HL_raw['Trade date'] = trade_date
    
    settle_date = HL_raw['Settle date']
    settle_date = [string_date_to_datetime(date) for date in settle_date]
    HL_raw['Settle date'] = settle_date
    
    #capitalise
    HL_raw['Reference'] = HL_raw['Reference'].str.upper()
    HL_raw['Description'] = HL_raw['Description'].str.upper()
    
    
    history = TransactionHistory()
    for index,transaction in HL_raw.iterrows():
        #print(index)
        #print(transaction)
        date = transaction['Settle date']
        transaction_type = transaction['Reference']
        value = transaction['Value (£)']
        description = transaction['Description']
        
        if(transaction_type == 'TRANSFER' or transaction_type == 'CARD WEB'):
            history.add_cash(value,date)
        elif(transaction_type == 'FPD'): #withdraw, but will be negative
            history.add_cash(value,date) 
        elif(transaction_type == 'LISA'):
            history.LISA_bonus(value,date)
        elif(transaction_type == 'INTEREST'):
            history.interest(value,date)
        elif(transaction_type == 'MANAGE FEE'):
            value = -1 * value
            history.fee(value,date)
        elif(transaction_type[0:4] == 'DRIB'):
            history.income_reinvestment(value,date)
            #should maybe change this too...
        elif(transaction_type[0] =='B' or transaction_type[0] =='S'):
            split = description.split('@') #will split it at the @ symbol
            price = float(split[-1])/100    #convert to GBP
            split = split[0].split()
            units = float(split[-1])
            split = split[:-1]
            description = ' '.join(split)
            
            
            
            #this checks for any differnce between the transaction value and the calculated value, which will be stamp duty or commission
            
            calc_val = round(price*units,2)
            value = abs(value)
            commission = round(abs(value - calc_val),2)
            
            if(commission != 0):
                history.commission(commission,date)
            
            HL_equity_name = general_functions.capitalize_and_underscore(description)
            if(initial_import):
                if HL_equity_name not in equities_list:
                    print('\''+ HL_equity_name + '\',')
                    equities_list.append(HL_equity_name)
                    
            else:
                current_equity = equities[HL_equity_name]
                    
                if(transaction_type[0] =='B'): #buy
                    history.buy_equity(current_equity, units, date,price=price)
                elif(transaction_type[0] =='S'): #sell
                    history.sell_equity(current_equity, units, date,price=price)
        else:
            #print("UNKNOWN TRANSACTION TYPE: " + transaction_type)
            pass
    
    if(initial_import):
        return equities_list
    else:
        return history