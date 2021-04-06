# -*- coding: utf-8 -*-
"""
Example 3:
    Shows the use of the fund and the transaction history modules.
"""

import equity
import datetime
from fund import Fund
import transaction_history
import analysis_functions
import data
import plot

#equities from data module
rightmove = data.rightmove
tesco = data.tesco
astrazeneca = data.astrazeneca
shell = data.shell

equity_dict = equity.EquityDict()
fund_launch_date = datetime.datetime(2018,1, 1)
equity_dict.add([rightmove,tesco])
proportions = {rightmove.name:1,tesco.name:2}
fund_1 = Fund.set_up_fund('fund 1',equity_dict,proportions,fund_launch_date)

history = transaction_history.TransactionHistory();


history.buy_equity(astrazeneca,1,datetime.datetime(2018,1, 1))
history.buy_equity(shell,1,datetime.datetime(2018,1, 1))
history.buy_equity(fund_1,5,datetime.datetime(2018,1, 1))
final_portfolio = history.portfolio()

fund_data = fund_1.get_holdings_data(datetime.datetime(2018,1, 1), datetime.datetime(2020,1, 1))
fund_data = analysis_functions.percent_change(fund_data)

data = final_portfolio.get_holdings_data(datetime.datetime(2018,1, 1), datetime.datetime(2020,1, 1))
data = analysis_functions.percent_change(data)

plot.line(data,axis = 'percentage')