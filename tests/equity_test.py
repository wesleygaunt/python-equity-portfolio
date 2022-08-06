# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 20:27:37 2020

@author: Test
"""
import equity
import constants
import analysis_functions
import datetime
import pandas as pd
from matplotlib import pyplot as plt
import general_functions
import time
#from data import jupiter_uk_smaller_companies as current_equity
#equity_dict = equity.EquityDict()


jupiter_uk_smaller_companies = equity.Equity(name = 'Jupiter UK Smaller Companies I ACC',ISIN='GB00B3LRRF45',provider='morningstar',provider_code='F00000OSWK]2]0]FOGBR$$ALL',unit = 'GBP',equity_type='fund')
#current_equity = jupiter_uk_smaller_companies

#eq = equity_dict.get_equity('Jupiter UK Smaller Companies I ACC')

#data_jupiter = jupiter_uk_smaller_companies.get_close_data(start_date = datetime.datetime(2020, 7, 2), end_date = datetime.datetime(2020, 7, 31))

#close_column_jupiter = data_jupiter.loc[:,'Close']

#data_jupiter = data_jupiter.rename(columns={'Close':jupiter_uk_smaller_companies.name})
#data_jupiter['Close'] = close_column_jupiter



#data_1 = baillie_american_2.get_data(start_date = start, end_date = end)
#jupiter_uk_smaller_companies_data = jupiter_uk_smaller_companies.get_data(start_date = start, end_date = end)
#fidelity_global_tech_data = fidelity_global_tech.get_data(start_date = start, end_date = end)
#baillie_american_data = baillie_american.get_data(start_date = start, end_date = end)
#baillie_american_2_data = baillie_american_2.get_data(start_date = start, end_date = end)
#legg_mason_japan_data = legg_mason_japan.get_data(start_date = start, end_date = end)


#data_2 = baillie_american_2.get_data(start_date = start, end_date = end)
#all_data = equity_dict.get_data(start)



#new_year = datetime.datetime(2020, 1, 1)
#data_single = baillie_american.get_data(new_year)
#new_equity.get_close_data(date)['Close'][0]
#close = data['Close']
#data.columns = ['']


#baillie_american_data = analysis_functions.percent_change(baillie_american_data,method = analysis_functions.FROM_FIRST_ITEM)
#baillie_american_2_data = analysis_functions.percent_change(baillie_american_2_data)
#baillie_american_2_data = analysis_functions.percent_change(baillie_american_2_data)



#data_2 = analysis_functions.percent_change(data_2)

#plt.plot(baillie_american_data)
start = datetime.datetime(2000, 1,1)
end = datetime.datetime(2020, 11, 30)

jupiter_uk_smaller_companies.get_data(start_date = start, end_date = end)

#baillie_american.save_equity()

print(0,flush = True)
data_0 = jupiter_uk_smaller_companies.get_data()

print(1)

start_1 = datetime.datetime(year = 2016,month = 1,day = 11) #open
end_1 = datetime.datetime(year = 2017,month = 10,day = 30) #open
data_1 = jupiter_uk_smaller_companies.get_data(start_date = start_1, end_date = end_1) #both open period

print(2)

start_2 = datetime.datetime(year = 2012,month = 5,day = 11)
end_2 = datetime.datetime(year = 2012,month = 5,day = 11)
data_2 = jupiter_uk_smaller_companies.get_data(start_date = start_2, end_date = end_2) #open 1 day
print(3)

start_3 = datetime.datetime(year = 1970,month = 5,day = 11)
end_3 = datetime.datetime(year = 2012,month = 5,day = 11)
data_3 = jupiter_uk_smaller_companies.get_data(start_date = start_3, end_date = end_3) #no start, open end

print(4)

start_4 = datetime.datetime(year = 2012,month = 5,day = 11)
end_4 = datetime.datetime(year = 2024,month = 5,day = 11)
data_4 = jupiter_uk_smaller_companies.get_data(start_date = start_4, end_date = end_4) #start available, end in the future

print(5)

start_5 = datetime.datetime(year = 2012,month = 5,day = 11)
data_5 = jupiter_uk_smaller_companies.get_data(start_date = start_5, end_date = None) #start available, no end. should return single day

#data = analysis_functions.percent_change(data,method = analysis_functions.FROM_FIRST_ITEM)
#plt.plot(data)