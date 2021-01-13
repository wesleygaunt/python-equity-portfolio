# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 10:42:03 2021

@author: Test
"""

# -*- coding: utf-8 -*-

import constants
from datetime import datetime
from HL_import import HL_import
import plot 

from data import HL_equities

#############################################################################

ISA_history = HL_import(filename = constants.DEFAULT_DATA_FOLDER + '\\ISA.csv',equities=HL_equities,initial_import = False)

final_ISA = ISA_history.portfolio()

ISA_annual_performance = ISA_history.annual_performance(datetime(2021,1,1))
ISA_entire_change = ISA_history.percentage_change(datetime(2021,1,1))

plot.line(ISA_entire_change,title = 'ISA_entire_change', axis = 'percentage')


final_ISA_data = final_ISA.get_holdings_data(datetime(2017,7,20), datetime(2021,1,7),total_column=False)

plot.line(final_ISA_data,title = 'Final ISA Portfolio', axis = 'value')
