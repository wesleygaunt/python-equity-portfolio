import constants
from datetime import datetime
import analysis_functions
from hl_import import hl_import
import plot 
import pandas as pd

from data import HL_equities
import data

print("ISA")
ISA_history = hl_import(filename = constants.DEFAULT_DATA_FOLDER + '\\ISA.csv',equities=HL_equities,initial_import = False)
print("LISA")
LISA_history = hl_import(filename = constants.DEFAULT_DATA_FOLDER + '\\LISA.csv',equities=HL_equities,initial_import = False)

final_LISA = LISA_history.portfolio()
final_ISA = ISA_history.portfolio()

#portfolio_dict = LISA_history.portfolio_dict()

#LISA_entire_percentage_change = LISA_history.entire_percentage_change(datetime(2021,1,7))
#plot.line(LISA_entire_percentage_change,title = "LISA_entire_percentage_change", axis = 'percentage')

#ISA_entire_percentage_change = ISA_history.percentage_change(datetime(2021,1,7))
LISA_annual_performance = LISA_history.annual_performance(datetime(2021,1,7))
ISA_annual_performance = ISA_history.annual_performance(datetime(2021,1,7))

# plot.line(ISA_entire_percentage_change,title = "ISA_entire_percentage_change", axis = 'percentage')

# start_date = ISA_entire_percentage_change.index[0].to_pydatetime()
# end_date = ISA_entire_percentage_change.index[-1].to_pydatetime()

# eq_dict = ISA_history.equity_dict
# eq_dict['ada'] = data.Halifax_FTSE100_Tracker
# equity_data = eq_dict.get_data(start_date,end_date)
# equity_data = analysis_functions.percent_change(equity_data)

# full_ISA_percentage_data = pd.concat([equity_data,ISA_entire_percentage_change],axis = 1)

# #plot.line(full_ISA_percentage_data,title = 'Full ISA History', axis = 'percentage')

# #final_LISA_data = final_LISA.get_holdings_data(datetime(2017,7,20), datetime(2021,1,7))
final_ISA_data = final_ISA.get_holdings_data(datetime(2017,7,20), datetime(2021,1,7),total_column=False)

# #plot.line(final_LISA_data,title = 'Final LISA Portfolio', axis = 'value')
plot.line(final_ISA_data,title = 'Final ISA Portfolio', axis = 'value')

# #del start_date, end_date