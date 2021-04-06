# -*- coding: utf-8 -*-
"""
The Fund class inherits from the Portfolio and the Equity classes. 
It bundles together equities (can be funds or stocks) into a wrapper.
The fund can be held in a portfolio, and plotted - same as a portfolio.

"""
from portfolio import Portfolio
from equity import Equity
import pandas as pd
import general_functions
import warnings
class Fund(Portfolio,Equity):   #multiple inheritance
    def __init__(self,init_name):
        
        
        Portfolio.__init__(self, name = init_name)
        Equity.__init__(self,name = init_name,try_to_load=False)
        
        #del self._Equity__name

        
        del self.provider
        del self.provider_code
        del self.symbol
    
    
    #override the name property. Was read only in equity.
    def __get_name(self):
        return self.__name
    
    def __set_name(self,name):
        self.__name = name
        pass
    
    """
    name is read only, so has controls on it.
    """
    name = property(__get_name,__set_name)
        
    
        
    @classmethod
    def set_up_fund(cls,name, equity_dict, proportion_orginal,fund_launch_date):
        """
        Initilizes a fund with the equities in equity_dict, and the proportions given in proportion_orignal.
        

        Parameters
        ----------
        cls : TYPE
            DESCRIPTION.
        name : str
            The new fund name
        equity_dict : equity.EquityDict
            Contains the equities that will form the fund.
        proportion_orginal : dict
            A dictionary with the equity names as keys, and proportions as values
            ie proportion_orginal = {astra_zeneca.name:1,ceres.name:1,anglo_asian.name:1}
        fund_launch_date : datetime.datetime
            The date which to initialize the fund (value = 1).

        Returns
        -------
        fund : fund.Fund
            The newly created fund.

        """
        fund = cls(name)
        ratio = proportion_orginal.copy()
        #fund.equity_dict = equity_dict.copy()

        total = sum(ratio.values())
        for key in ratio:
            equity = equity_dict[key]
            ratio[key] = ratio[key]/total
            fund.set_equity_by_value(equity,value = ratio[key],date = fund_launch_date)
        
        return fund
    

    #override the save function from 
    def save(self):
        print("fund save method not yet implemented")
        
        
    def get_data(self,start_date,end_date):#overrides the Equity.get_data_metho
        """
        Gets the historical data of the fund, either by making a request, using data in memory or loading it from storage.

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
        
        data = self.get_holdings_data(start_date,end_date)
        data = data['TOTAL']
        data = pd.DataFrame(data)
        data.columns = [self.name]

        return data
    