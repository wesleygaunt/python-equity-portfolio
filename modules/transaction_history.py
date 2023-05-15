# -*- coding: utf-8 -*-
"""
The transaction history class holds a record of equity purchases. 
The portfolio method below can create portfolios and specific times in the history, to allow historical analysis.
"""

import pandas as pd
import datetime
import equity
import portfolio
import numpy as np
import analysis_functions
__MINDATE = datetime.datetime(1900,1, 1)

BY_VALUE = 0
BY_UNITS = 1
BY_PROPORTION_OF_EQUITY_HOLDING = 2
BY_PROPORTION_OF_CASH_HOLDING = 3

class TransactionHistory:
    def __init__(self):
        self.transaction_data = pd.DataFrame({"date":[],
                                              "equity":[],
                                              "action":[],
                                              "units":[],
                                              "price per unit":[],
                                              "value":[]})
        
        self.equity_dict = equity.EquityDict()
        
        self.current_portfolio = None
        
        

    
    def __sort_history(self):     
        """
        sorts transaction data by date
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
        uses merge sort as this is guarenteed to keep order of equal elements
        and so the equity to cash and cash to equity conversions will still appear in the correct order.

        Returns
        -------
        None.

        """
        #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
        #uses merge sort as this is guarenteed to keep order of equal elements, and so the equity to cash and cash to equity conversions will still appear in the correct order
        self.transaction_data.sort_values(by=["date"],kind = 'mergesort',inplace=True)        #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
        self.transaction_data.reset_index(drop = True, inplace = True)


    def __equity_type_check(self,item):
        """
        Will raise a TypeError unless an equity or fund is passed.

        Parameters
        ----------
        equity_to_check : any
            DESCRIPTION.

        Raises
        ------
        TypeError
            Raised if a type other than equity or fund is passed.

        Returns
        -------
        None.

        """
        
        if (isinstance(item, equity.Equity)):
            return 
        else:
            raise TypeError("Pass an equity or fund to Portfolio")
            return   
    
    def buy_equity(self,equity,date, method = BY_VALUE, units = None, value = None, proportion_of_cash_to_buy = None):
        """
        Buy an equity on a given dates. This method operates via two methods:
            BUY_EQUITY_BY_VALUE: Buys the given equity at the total value given by 'value'.
            BUY_EQUITY_BY_UNITS: Buys the given units of the equity, given by 'units'

        Parameters
        ----------
        quity : equity.Equity
            Equity to buy.
        date : datetime.datetime
            The date to make the transaction on.
        method : int, optional
            DESCRIPTION. The default is BUY_EQUITY_BY_VALUE.
        units : numeric, optional
            Number of units to buy. The default is None.
        value : numeric, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        
        
        self.__equity_type_check(equity)
        
        
        self.equity_dict.add(equity)
        price = equity.get_data(date,date).iloc[0][0] #will be in pence!

        if(method == BY_VALUE):
            
            #equity_price_data = new_equity.get_data(date,date)  #value in GBp
            #date = equity_price_data[equity.name].index[0]
            #equity_price = equity_price_data[equity.name][date]
            #units = value/equity_price
            units = value/price
        elif(method == BY_UNITS):
            units = units
        elif(method == BY_PROPORTION_OF_CASH_HOLDING):
            need to work out cash value...
        else:
            return

        cash_value = -1 * units * price #negative as cash is going down
        

        buy_transaction = {"equity": equity.name, 
                           "action":"buy_equity", 
                           "units": units,
                           "date":date,
                           "price per unit":price,
                           "value":(cash_value)}
      
        self.transaction_data = self.transaction_data.append(buy_transaction,ignore_index=True)
        
        self.current_portfolio = self.portfolio()

        
            
    def sell_equity(self,equity,date, method = BY_VALUE, units_to_sell = None,value_to_sell = None, proportion_to_sell = None):      
        """
        Sells an equity at the date specified.


        Parameters
        ----------
        new_equity : equity.Equity
            Equity to sell.
        units : int or float
            Number of units to sell.
        date : datetime.datetime
            The date to make the transaction on.
        price : int, optional
            If set, will override the price obtained using the date. The default is None.

        Returns
        -------
        None.

        """
        self.__equity_type_check(equity)
        self.equity_dict.add(equity)
        price = equity.get_close(date).iloc[0][0]  #will be in pence!
        
        currently_held_units = self.current_portfolio[equity]
        currently_held_value= currently_held_units * price
        
        if(method == BY_VALUE):
            if(currently_held_value < value_to_sell):
                units_to_sell = currently_held_units #sell all
            else:
                units_to_sell = value_to_sell/price 
        elif(method == BY_UNITS):
            if(currently_held_units < units_to_sell):
                units_to_sell = currently_held_units #sell all
            else:
               units_to_sell = units_to_sell 
        elif(method == BY_PROPORTION_OF_EQUITY_HOLDING):
            if(proportion_to_sell < 0):
                proportion_to_sell = 0
            elif(proportion_to_sell > 1):
                proportion_to_sell = 1
            units_to_sell = proportion_to_sell * (value_to_sell/price)     
            
        else:
            return
            

        cash_value = units_to_sell * price
        
        sell_transaction = {"equity": equity.name, 
                            "action":"sell_equity", 
                            "units": units_to_sell,
                            "date":date,
                            "price per unit":price,
                            "value":cash_value}

        self.transaction_data = self.transaction_data.append(sell_transaction,ignore_index=True)
        
        self.current_portfolio = self.portfolio()
            
    def add_cash(self,units,date):
        """
        Adds cash.

        Parameters
        ----------
        units : int or float
            Amount of cash to add, in GBP.
        date : datetime.datetime
            Date to add cash on.

        Returns
        -------
        None.

        """
        #units = abs(units)

        if(units == 0):
            return
        buy_transaction = {"equity": np.nan, 
                           "action":"add_cash", 
                           "units": units,
                           "date":date,
                           "price per unit":1,
                           "value":units}
        self.transaction_data = self.transaction_data.append(buy_transaction,ignore_index=True)        
        return
    
    def LISA_bonus(self,units,date):
        """
        Adds LISA bonus.

        Parameters
        ----------
        units : int or float
            Amount of cash to add, in GBP.
        date : datetime.datetime
            Date to add cash on.

        Returns
        -------
        None.

        """
        if(units == 0):
            return
        buy_transaction = {"equity": np.nan, 
                           "action":"LISA_bonus", 
                           "units": units,
                           "date":date,
                           "price per unit":1,
                           "value":units}
        self.transaction_data = self.transaction_data.append(buy_transaction,ignore_index=True)        
        return
    
    def interest(self,units,date):
        """
        Adds interest.

        Parameters
        ----------
        units : int or float
            Amount of interest to add, in GBP.
        date : datetime.datetime
            Date to add cash on.

        Returns
        -------
        None.

        """
        if(units == 0):
            return
        transaction = {"equity": np.nan, 
                           "action":"interest", 
                           "units": units,
                           "date":date,
                           "price per unit":1,
                           "value":units}
        self.transaction_data = self.transaction_data.append(transaction,ignore_index=True)        
        return
    
    def income_reinvestment(self,units,date):
        """
        Adds cash.

        Parameters
        ----------
        units : int or float
            Amount of cash to add, in GBP.
        date : datetime.datetime
            Date to add cash on.

        Returns
        -------
        None.

        """
        if(units == 0):
            return
        buy_transaction = {"equity": np.nan, 
                           "action":"income_reinvestment", 
                           "units": units,
                           "date":date,
                           "price per unit":1,
                           "value":units}
        self.transaction_data = self.transaction_data.append(buy_transaction,ignore_index=True)        
        return
    
    def fee(self,units,date):
        """
        Takes fee.

        Parameters
        ----------
        units : int or float
            Amount of fee to pay, in GBP.
        date : datetime.datetime
            Date to add cash on.

        Returns
        -------
        None.

        """
        
        if(units == 0):
            return
        transaction = {"equity": np.nan, 
                           "action":"fee", 
                           "units": units,
                           "date":date,
                           "price per unit":1,
                           "value":-1*units}
        self.transaction_data = self.transaction_data.append(transaction,ignore_index=True)        
        return
    
    def commission(self,units,date):
        """
        Adds commission.

        Parameters
        ----------
        units : int or float
            Amount of fee to pay, in GBP.
        date : datetime.datetime
            Date to add cash on.

        Returns
        -------
        None.

        """
        
        if(units == 0):
            return
        transaction = {"equity": np.nan, 
                           "action":"commission", 
                           "units": units,
                           "date":date,
                           "price per unit":1,
                           "value":-1*units}
        self.transaction_data = self.transaction_data.append(transaction,ignore_index=True)        
        return
    
    
        
   
    def withdraw_cash(self,units,date):
        """
        Withdraws cash.

        Parameters
        ----------
        units : int or float
            Amount of cash to add, in GBP.
        date : datetime.datetime
            Date to add cash on.

        Returns
        -------
        None.

        """
        units = abs(units)
        if(units == 0):
            return
        buy_transaction = {"equity": np.nan, 
                           "action":"withdraw_cash", 
                           "units": units,
                           "date":date,
                           "price per unit":1,
                           "value":-1 * units}
        self.transaction_data = self.transaction_data.append(buy_transaction,ignore_index=True)
        
        

    def portfolio(self,end_date = None):
        """
        Generates a portfolio at a certain date from the transaction history.


        Parameters
        ----------
        end_date : datetime.datetime, optional
            Date of when to create the portfolio, if None will default to final portfolio. The default is None.

        Returns
        -------
        new_portfolio : TYPE
            DESCRIPTION.

        """
        new_portfolio = portfolio.Portfolio();   #need to copy this, gonna require a LOT of memory later on...
            
        self.__sort_history()                           #sort the transaction history

        
        #The next lines throw a FutureWarning: https://stackoverflow.com/questions/40659212/futurewarning-elementwise-comparison-failed-returning-scalar-but-in-the-futur
        #H
        all_dates = self.transaction_data['date']#series object of all the dates
        
        #if the end date is not defined, use the final date available
        if(end_date == None):
            end_date = all_dates.tolist()[-1]
            
            
        #select the relavent transaction rows    
        relavent_dates = all_dates[(all_dates <= end_date)]    #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#the-query-method 
        relavent_dates_index_list = relavent_dates.index.tolist()                      #will contain the indices of the dates relavent to the selection
        relavent_transactions = self.transaction_data[relavent_dates_index_list[0]:relavent_dates_index_list[-1]+1]
        
        relavent_transactions.reset_index(drop = True, inplace = True)

      
        #https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
        #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html
        
        for index, transaction_row in relavent_transactions.iterrows():  #https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas        
            
            action = transaction_row['action']
            units = transaction_row['units']
            value = round(transaction_row['value'],2)
            new_portfolio.change_cash(value)

            if((action == 'buy_equity') or (action == 'sell_equity')):
                equity_name = transaction_row['equity']
                equity = self.equity_dict[equity_name]      #get the original equity from the name
                
                if(action == 'buy_equity'):
                    new_portfolio.change_equity_by_units(equity, units)  
                    
                elif(action == 'sell_equity'):
                    new_portfolio.change_equity_by_units(equity, -1 * units)               
        
        return new_portfolio  
    
    def portfolio_dict(self,end_date = None):
        """
        Creates a dictionary of all the different portfolios that have been held

        Returns
        -------
        portfolio_dict : TYPE
            DESCRIPTION.

        """
        
        all_dates = self.transaction_data['date']#series object of all the dates
        
        #if the end date is not defined, use the final date available
        if(end_date == None):
            end_date = all_dates.tolist()[-1]
            
            
        #select the relavent transaction rows    
        relavent_dates = all_dates[(all_dates <= end_date)]    #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#the-query-method 
        relavent_dates_index_list = relavent_dates.index.tolist()                      #will contain the indices of the dates relavent to the selection
        relavent_transactions = self.transaction_data[relavent_dates_index_list[0]:relavent_dates_index_list[-1]+1]
        
        relavent_transactions.reset_index(drop = True, inplace = True)

      
        
        
        dates = self.transaction_data['date']#series object of all the dates
        start_date = dates[0].to_pydatetime()
        
        portfolio_dict = {}       
        for index,transaction_row in relavent_transactions.iterrows():            
            action = transaction_row['action']
            if((action == 'buy_equity') or (action == 'sell_equity')):
                end_date = dates[index].to_pydatetime()
                #print(str(start_date) + '...'+str(end_date))
                portfolio = self.portfolio(start_date)
                
                portfolio_dict[start_date] = portfolio

                start_date = end_date
                
                
                
        portfolio = self.portfolio(start_date)
        portfolio_dict[start_date] = portfolio
            
        return portfolio_dict
    
    def percentage_change(self,final_date):
        portfolio_dict = self.portfolio_dict(final_date)
        dates = list(portfolio_dict.keys())
        dates.sort()
        no_dates = len(dates)
        
        data = pd.DataFrame()
                
        final_value = 1
        
        for index in range(no_dates):
            start_date = dates[index]
            if(start_date == dates[-1]):
                #if final date
                end_date = final_date
            else:
                end_date = dates[index + 1]
                
            #print(str(start_date) + ', ' +str(end_date))
            portfolio = portfolio_dict[start_date]
            portfolio_data = portfolio.get_percentage_change_data(start_date, end_date)
            portfolio_data = final_value * portfolio_data
            data = data.append(portfolio_data,verify_integrity=False) #will have overlaps!
            
            if(portfolio_data.empty == False):
                    final_value = portfolio_data.iloc[-1]
            
        return data
    
    def annual_performance(self,final_date):
        percentage_change = self.percentage_change(final_date)
        return analysis_functions.annual_performance(percentage_change)
