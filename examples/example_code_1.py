# -*- coding: utf-8 -*-
"""
Example 1:
    
    Shows the use of the equity module, which contains the Equity and EquityDict classes. Also showcases 
    the analysis_functions module. Plots data.
    
    This will save data to a local folder, specified in the constants module.

"""
import equity
import analysis_functions
import datetime
import data
import plot


#set up the equities
rightmove = data.rightmove
tesco = data.tesco
astrazeneca = data.astrazeneca
shell = data.shell

#get data, note as the data on 2020 12 5 is not available, the next available data point is returned.
rightmove_single_day = rightmove.get_data(start_date = datetime.datetime(2020, 12, 5), end_date = datetime.datetime(2020, 12, 5))
rightmove_period = rightmove.get_data(start_date = datetime.datetime(2010, 12, 22), end_date = datetime.datetime(2020, 12, 5))

#can use the percentage change function to normalise the data to 1 at the beginning of the period. 
rightmove_period_percentage = analysis_functions.percent_change(rightmove_period)

#more equities, from 

#reload equity, to showcase the data saving and reloading

#set up an EquityDict to hold multiple equities
equity_dict = equity.EquityDict()
equity_dict.add([rightmove,astrazeneca,tesco])

#can also set by dict methods, note how the name is reset
equity_dict['key will be modified'] = shell
equity_from_dict = equity_dict['Royal Dutch Shell plc'] #examine in command line if required.


#same can be done for the equitydict
dict_data_single_day = equity_dict.get_data(start_date = datetime.datetime(2020, 10, 19), end_date = datetime.datetime(2020, 10, 19))
dict_data_period = equity_dict.get_data(start_date = datetime.datetime(2010, 11, 5), end_date = datetime.datetime(2016, 4, 9))


dict_data_percentage = analysis_functions.percent_change(dict_data_period)
#plots data, all given equity datas are plotted the same way.
plot.line(dict_data_percentage, axis = 'percentage')