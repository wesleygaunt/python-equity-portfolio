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

__MINDATE = datetime.datetime(1900,1, 1)

class TransactionHistory:
    def __init__(self):
        self.transaction_data = pd.DataFrame({"date":[],
                                              "equity":[],
                                              "action":[],
                                              "units":[],
                                              "price per unit":[],
                                              "value":[]})
        
        self.equity_dict = equity.EquityDict()
        
        

    
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


    def __equity_type_check(self,equity_to_check):
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
        import fund          #imported here to prevent circular inclusion errors.

        if (type(equity_to_check) == equity.Equity or type(equity_to_check) == fund.Fund):
            return 
        else:
            raise TypeError("Pass an equity or fund to Portfolio")
            return   
    
    def buy_equity(self,new_equity,units,date,price = None):
        """
        Buys an equity at the date specified.

        Parameters
        ----------
        new_equity : equity.Equity
            Equity to buy.
        units : int or float
            Number of units to buy.
        date : datetime.datetime
            The date to make the transaction on.
        price : int, optional
            If set, will override the price obtained using the date. The default is None.

        Returns
        -------
        None.

        """
            
        self.__equity_type_check(new_equity)
        
        
        self.equity_dict.add_equity(new_equity)
        if(price == None):
            price = new_equity.get_data(date,date).iloc[0][0] #will be in pence!

        cash_value = -1 * units * price #negative as cash is going down
        
        new_equity_name = str(new_equity)
        buy_transaction = {"equity": new_equity_name, 
                           "action":"buy_equity", 
                           "units": units,
                           "date":date,
                           "price per unit":price,
                           "value":(cash_value)}
      
        self.transaction_data = self.transaction_data.append(buy_transaction,ignore_index=True)

        
            
    def sell_equity(self,new_equity,units,date,price = None):      
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
        self.__equity_type_check(new_equity)
        self.equity_dict.add_equity(new_equity)
        
        
        
        if(price == None):
            price = new_equity.get_close(date).iloc[0][0]  #will be in pence!
            
        new_equity_name = str(new_equity)

        cash_value = units * price
        
        sell_transaction = {"equity": new_equity_name, 
                            "action":"sell_equity", 
                            "units": units,
                            "date":date,
                            "price per unit":price,
                            "value":cash_value}

        self.transaction_data = self.transaction_data.append(sell_transaction,ignore_index=True)

            
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
        
        

    def portfolio(self,end_date = None,name = ''):
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
        new_portfolio = portfolio.Portfolio(name);   #need to copy this, gonna require a LOT of memory later on...
            
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
    
    def entire_percentage_change(self,final_date):
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
