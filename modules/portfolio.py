# -*- coding: utf-8 -*-
"""
The portfolio class holds equities and quantities in a dataframe, along with cash. It has no memory, but can be created from the transaction history class. 
"""
import pandas as pd
import warnings
import equity
import analysis_functions
import general_functions

class Portfolio:
    
    def __init__(self):
        self.cash = 0.0
        self.holdings = pd.DataFrame({"equity":[],"units":[]})
        self.holdings = self.holdings.set_index('equity')
        self.equity_dict = equity.EquityDict()
        
    
    
    #https://stackoverflow.com/questions/141545/how-to-overload-init-method-based-on-argument-type
    @classmethod
    def fromTransactionHistory(cls, transaction_history,date = None):
        """
        Create a Portfolio object from a transaction history. Will create a portfolio as it looked at the date specified

        Parameters
        ----------
        cls : TYPE
            DESCRIPTION.
        transaction_history : TransactionHistory
            The transaction history object which will create the portofolio.
        date : datetime.datetime, optional
            The date to create the portfolo at. The default is None.

        Returns
        -------
        new_portfolio : Portfolio
            The new portolfolio.

        """
        if(date == None):
            new_portfolio = transaction_history.final_portfolio()        
        else:
            new_portfolio = transaction_history.portfolio(date)
        return new_portfolio

    def __equity_type_check(self,equity_to_check):
        import fund

        """
        Will raise a TypeError unless an equity is passed.

        Parameters
        ----------
        equity_to_check : TYPE
            DESCRIPTION.

        Raises
        ------
        TypeError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if (type(equity_to_check) == equity.Equity or type(equity_to_check) == fund.Fund):
            return 
        else:
            raise TypeError("Pass an equity or fund to Portfolio")
            return    
        
    #magic methods
    def __init_equity(self,equity):     
        """
        This will create a new row in the portfolio with 0 units, and can also be used to 'reset' a equity count.

        Parameters
        ----------
        equity : equity.Equity
            Equity to initialise.

        Returns
        -------
        None.

        """
        
        self.holdings.loc[equity.name] = 0

        self.equity_dict.add(equity)
   
    def __clean_portfolio(self):
        """
        Delete rows that show 0 units.

        Returns
        -------
        None
            DESCRIPTION.

        """
        units_column = self.holdings['units']   
        equities_with_no_units = units_column[units_column < 0.001].index.tolist() 
        
        if equities_with_no_units == []:
            return 
        
        else:
            for equity_name in equities_with_no_units:
                del self.equity_dict[equity_name]
            self.holdings.drop(index = equities_with_no_units, inplace = True)
            return
             
    def __len__(self):
        return len(self.holdings)   
        
    def __getitem__(self, equity_input):
        """
        Gets the number of units of a certain equity. Will not raise a KeyError, but will return 0 if the specified equity does not exist.

        Parameters
        ----------
        equity : Equity
            The equity to check.

        Returns
        -------
        int
            The number of units in the portfolio.

        """
        if(type(equity_input) == str):
            name = equity_input
        elif(type(equity_input) == equity.Equity):
            name = equity_input.name
        else:
            return 0
        
        if(name in self.holdings.index):
            units_col = self.holdings['units']
            return units_col[name]
        else:
            return 0 #if the equity doesn't exist, return 0 (no equities)
    
    def __setitem__(self,equity, units):
        """
        Sets the value in the portfolio of a certain equity.

        Parameters
        ----------
        equity : TYPE
            DESCRIPTION.
        units : TYPE
            DESCRIPTION.

        Raises
        ------
        a
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.__equity_type_check(equity)    #will raise a type error if it fails
        
        if((equity.name in self.holdings.index) == False):   #if it doesn't already exist
            self.__init_equity(equity)    #create it first
        if (units < 0):
            warnings.warn(equity.name + " = " + str(units),category = UserWarning,stacklevel=4)
        
        self.holdings.at[equity.name, 'units'] = units     #https://stackoverflow.com/questions/13842088/set-value-for-particular-cell-in-pandas-dataframe-using-index     
        self.__clean_portfolio()                   
    
    def __delitem__(self,equity):
        """
        Deletes the equity from the portfolio


        Parameters
        ----------
        equity : TYPE
            DESCRIPTION.

        Raises
        ------
        a
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.__equity_type_check(equity)    #will raise a type error
        if (equity.name in self.holdings.index):
            self.holdings.drop(index = equity.name,inplace = True)
            del self.equity_dict[equity.name]
            #self.equity_dict.remove_equity(equity)
            return
        else:
            return
        
    def set_equity_by_value(self,equity,value,date):
        """
        Sets the number of equities by value specified, at the date specified. ie if at a certain date, a certain equity has value 5 GBP
        and value = 10, the function will set the number of units held as 2.

        Parameters
        ----------
        equity : equity.Equity
            DESCRIPTION.
        value : int
            DESCRIPTION.
        date : datetime.datetime
            DESCRIPTION.

        Returns
        -------
        None.

        """
        dataframe = equity.get_data(date,date)  #value in GBp
        date = dataframe[equity.name].index[0]
        equity_value = dataframe[equity.name][date]
        units = value/equity_value
        self[equity] = units
        return
        
                       
    def change_equity_by_units(self, equity, units_to_change):
        """
        This will either add or subract units to an equity.
        Parameters
        ----------
        equity : TYPE
            DESCRIPTION.
        units_to_change : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self[equity] = self[equity] + units_to_change
        
        # if(self[equity] <= 0.001):
        #     del self[equity]
        return
        
      

    def get_holdings_data(self, start_date = None, end_date = None, total_column = True):
        """
        Gets the value data of all the holdings in the portfolio between the dates specified.

        Parameters
        ----------
        start_date : TYPE
            DESCRIPTION.
        end_date : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        portfolio_value_data : TYPE
            DESCRIPTION.

        """
        portfolio_value_data = pd.DataFrame()
        
        
        eq_close_data = self.equity_dict.get_data(start_date, end_date)
        
    
        
        eq_close_data = general_functions.ensure_datetime_index(eq_close_data)
            
        
        for equity_name in self.equity_dict:
            
            #eq = self.equity_dict[equity_name]
            no_eq_units = self[equity_name]      #get number of units of the equity
            
            eq_value_data = pd.DataFrame(eq_close_data[equity_name]) * no_eq_units            
            portfolio_value_data = portfolio_value_data.add(eq_value_data, fill_value = 0)
        
        portfolio_value_data.fillna(method = 'ffill', inplace = True)         #need to fill in the blanks
        
        #add a sum column.
        if(total_column):
            portfolio_value_data['TOTAL'] = portfolio_value_data.sum(axis = 1)
        
        return portfolio_value_data


    def get_data(self,start_date = None ,end_date = None):
        """
        Gets the historical data of the portfolio, either by making a request, using data in memory or loading it from storage.

        Parameters
        ----------
        start_date : datetime.datetime
            Start date of the data to request.
        end_date : datetime.datetime
            End date of the data to request.

        Returns
        -------
        data : pandas.DataFrame
            Historical data dataframe.
        """
        data = self.get_holdings_data(start_date,end_date, total_column = True)
        data = data['TOTAL']
        
        
        data = pd.DataFrame(data)
        self.data = data
            
        return data
    
    def get_percentage_change_data(self,start_date = None,end_date = None):
        if(start_date == end_date):
            d = {'Date':[start_date],'TOTAL':[1]}
            data = pd.DataFrame(d)
            data.set_index('Date', inplace=True)
            return data
        else:
            data = self.get_data(start_date, end_date)
            data = analysis_functions.percent_change_from_beginning(data)
            return data
        
    def annual_performance(self, start_date = None ,end_date = None):
        data = self.get_data(start_date,end_date)
        
        annual_performance_data = analysis_functions.annual_performance(data)
        
        return annual_performance_data
        
        
    def change_cash(self,value):
        value = round(value,2)
        self.cash = round(self.cash + value,2)
        return