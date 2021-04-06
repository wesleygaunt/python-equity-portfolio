# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 10:55:32 2021

@author: Test
"""

import plot
import datetime
import momentum
import data

start = datetime.datetime(2010,1,1)
end = datetime.datetime(2021,1,1)

equity_dict = data.funds

#data = equity_dict.get_data(start,end)
#percent_data = analysis_functions.percent_change(data,analysis_functions.FROM_FIRST_ITEM)
#plot.line(percent_data)

percent_data_full = momentum.momentum(equity_dict,6, start_date = start,end_date = end);
plot.line(percent_data_full)