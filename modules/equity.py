# -*- coding: utf-8 -*-
"""
The equity module contains 2 basic building blocks of the project, Equity and EquityDict.

Equity: This is the fundamental building block, and contains infomation about a specific stock or fund, used to request historical data and save it to the local system.
EquityDict: Inherits from the dictionary class - holds equities and requests historical data from mutliple equities at once.

"""
import datetime
from data_requests import request_hist_data
import general_functions
import pandas as pd
import constants
import json
import analysis_functions

class Equity:
    def __init__(self, 
                name,
                ISIN = '',
                symbol = '',
                provider = '',
                provider_code = '',
                unit = '',
                equity_type = '',
                try_to_load = True):
        
        self.data = pd.DataFrame()
        self.__name = general_functions.capitalize_and_underscore(name)       #private, as not to be edited accidentally
    
        self.equity_filename = constants.DEFAULT_DATA_FOLDER + '\\' +self.__name + '.json' #where the equity metadata will be saved
        self.historical_data_filename = constants.DEFAULT_DATA_FOLDER + '\\' + self.__name + "_hist_data.json"
        #first try to load
        if try_to_load:
            try:
                file = open(self.equity_filename)
                JSON_dict = json.load(file)
                file.close()
                self.__dict__ = JSON_dict
                
                self.data = pd.DataFrame()
                self.saved_data_start_date = datetime.datetime.fromisoformat(self.saved_data_start_date)
                self.saved_data_end_date = datetime.datetime.fromisoformat(self.saved_data_end_date)
                

                
                print("loaded equity: " + self.__name)
            
            except:
                print('load failed: ' + self.__name)
                try_to_load = False #will force this into the other branch
            
        if(try_to_load == False):      
            self.__name = general_functions.capitalize_and_underscore(name)       #private, as not to be edited accidentally
            
            self.ISIN = general_functions.convert_to_ISIN(ISIN)                 #private, as not to be edited accidentally
    
            self.symbol = symbol #ie ticker, MSFT
            self.provider = provider 
            self.provider_code = provider_code
            self.unit = unit            #ie GBp
                
            
            self.equity_type = equity_type
            
            self.saved_data_available = False
            self.saved_data_start_date = constants.MIN_DATE
            self.saved_data_end_date = constants.MIN_DATE
            
            self.save_equity()
                                
               
    
    def get_JSON_dict(self):
        JSON_dict = self.__dict__.copy()
        to_remove = []
        for name in JSON_dict:
            var = JSON_dict[name]
            if(type(var) == pd.DataFrame):
                #print(name + ': DataFrame')
                to_remove.append(name)
            elif(type(var) == datetime.datetime):
                #print(name + ': Datetime')
                JSON_dict[name] = JSON_dict[name].isoformat()
                
        for name in to_remove:
            del JSON_dict[name]

        return JSON_dict
    def save_equity(self):
        """
        This saves the equity metadata (not the historical data) to a JSON so it can be loaded at a later time.

        Returns
        -------
        filename : String
            The filename of the file that metadata has been saved to.

        """
        

        JSON_dict = self.get_JSON_dict()
        with open(self.equity_filename, 'w') as file:
            json.dump(JSON_dict, file)
        
        print("equity saved: "+ self.__name)
        return self.equity_filename
    
    
    def load_historical_data(self):
        """
        Loads the historical data from a JSON, will load into self.data.

        Returns
        -------
        None.

        """
        print('loaded historical data: ' + self.historical_data_filename)
        self.data = pd.read_json(self.historical_data_filename)
        self.data = self.data.sort_index()
        #self.data.index.names = ['Date']
        pass
    
    def save_historical_data(self):
        """
        Saves the historical data to a JSON, will save self.data.


        Returns
        -------
        None.

        """
        
        print('saved historical data: ' + self.historical_data_filename)
        if(self.data.empty == False):
            self.data = self.data.sort_index()

            self.data.to_json(self.historical_data_filename,date_format='epoch')
            self.saved_data_available = True
            self.saved_data_start_date = self.data.index[0].to_pydatetime()
            self.saved_data_end_date = self.data.index[-1].to_pydatetime()
            self.save_equity()
        
        return
    
    def __get_name(self):
            return self.__name
    
    def __set_name(self,name):
        print("Unable to modify name")
        pass
    
    """
    name is read only, so has controls on it.
    """
    name = property(__get_name,__set_name) 
    
    def __request_data(self):
        """
        Requests data from internet using requests module

        Returns
        -------
        pandas.DataFrame
            The data that has been loaded.

        """
        print('request data: ' + self.name)
        self.data = request_hist_data(self.provider,self.provider_code, self.unit,constants.MIN_DATE,datetime.datetime.now())
        
        self.data.columns = [self.name] #remove names

        
        data_start_date = self.data.index[0].to_pydatetime()
        data_end_date = self.data.index[-1].to_pydatetime()
        
        self.data = self.data.reindex(pd.date_range(data_start_date, data_end_date), method = 'ffill')
        
        
        self.save_historical_data()
        
        return self.data
    
    def __make_data_available(self):
        
        #attempts to either load data locally or if not available requests it from the data source
        if(self.saved_data_available):
            self.new_request = False
            if(self.data.empty):    #if not yet loaded, load
                self.load_historical_data()
            else:
                pass #self.data contains the data
                  
        else:
            self.__request_data()
            self.new_request = True
        
        
    
    def get_data(self,start_date = None,end_date = None):
        """
        Gets the historical data of the equity, either by making a request, using data in memory or loading it from storage.

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
        if(end_date == None):
            end_date = start_date
        
        self.__make_data_available()
                 
        data = self.data.copy()
        
        if(start_date == None and end_date == None):
            return data
        
        
          

        if(self.saved_data_start_date <= start_date and start_date <= self.saved_data_end_date):
            #print('start_date available')
            pass
        else:   #if(self.saved_data_start_date > start_date):  
            #print('start_date not available, will return earliest data') 
            pass
             
        if(self.saved_data_start_date <= end_date and end_date <=  self.saved_data_end_date):
            #print('end_date available')
            pass
            
        # else:
        #     if(new_request == False):
        #         #the end date is not in the saved data AND we haven't just done a request.
        #         self.__request_data()
        #         new_request = True
        #         data = self.data
        #     data = data.reindex(pd.date_range(self.saved_data_start_date, end_date), method = 'ffill')

            
                
        elif(self.saved_data_end_date < end_date and self.new_request == False):
            #the end date is not in the saved data AND we haven't just done a request.
            
            self.__request_data()
            new_request = True

            data = self.data.copy()
            
        if(self.saved_data_end_date < end_date and new_request == True):
            #if still out of range
            
            #data = data.reindex(pd.date_range(self.saved_data_start_date, end_date), method = 'ffill')
            pass

            
        # else:
        #     #the end data isn't available,but we have up to date data (new_request == True)
        #     ##print("no new data")
        #     data = data.reindex(pd.date_range(self.saved_data_start_date, end_date), method = 'ffill')

        
        
        #nearest_date_before_start = general_functions.nearest_before(data.index,start_date)
        #nearest_date_after_end = general_functions.nearest_after(data.index,end_date)
        #print(nearest_date_before_start)
        #print(nearest_date_after_end)
        #data = data[nearest_date_before_start:nearest_date_after_end]
        data = data[start_date:end_date]

          
            
            
        
        #if(start_date == end_date):
         #   data = pd.DataFrame(data.loc[nearest_date_after_end])
        
        #if(data.shape[0] == 1):
         #   data = data.T
         
        return data   
        
            
        

    def __str__(self):
        return self.name          
    
    def annual_performance(self):
        """
        Calculates the annual performance of the equity

        Returns
        -------
        data_split_percentage : TYPE
            DESCRIPTION.

        """
        self.__make_data_available()
        
        
        annual_performance = analysis_functions.annual_performance(self.data)

        
        return annual_performance
        
class EquityDict(dict):
    def __init(self,*args, **kwargs):
        dict.__init__(*args, **kwargs)
        
    def __setitem__(self, key, item):
        key = item.name
        key = general_functions.capitalize_and_underscore(key)
        super(EquityDict,self).__setitem__(key,item)
    def __getitem__(self,key):
        key = general_functions.capitalize_and_underscore(key)
        return super(EquityDict,self).__getitem__(key)
    
    def add(self,arg):
        """
        Adds an equity (or list of equities) to the EquityDict. Sets up the keys correctly.

        Parameters
        ----------
        arg : Equity.equity or list
            The equity(s) to add.

        Returns
        -------
        None.

        """
        if(type(arg) == list):
            self.__add_multiple(arg)
            return
        else:
            self.__setitem__(arg.name,arg)
            return

    def __add_multiple(self,list_of_equities):
        for equity in list_of_equities:
            self.__setitem__(equity.name,equity)
        return
    
    def __delitem__(self,key):
        key = general_functions.capitalize_and_underscore(key)
        super(EquityDict,self).__delitem__(key)
        return
    
    def get_data(self,start_date,end_date = None):
        """
        Gets the close data for all the equities contained in the EquityDict.

        Parameters
        ----------
        start_date : datatime.datetime
            The start date to fetch data for
        end_date : datetime.datetime, optional
            The end date, if None will only return a single date. The default is None.

        Returns
        -------
        full_data : pandas.DataFrame
            The day close data.

        """
        
       
        full_data = pd.DataFrame()  #empty dataframe
        for eq in self.values():
            eq_data = eq.get_data(start_date, end_date)
            full_data = full_data.add(eq_data,fill_value = 0)
            
        full_data.fillna(method = 'ffill',inplace = True)      #forward fill to get rid of any discrepancies, where data is missing in one col, but not others
        
        if(full_data.shape[0] == 1): #transpose if required
            full_data = full_data.T
            
        return full_data


