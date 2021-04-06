# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import time

#my modules
import analysis_functions
import data_requests
import equity

from portfolio import Portfolio
from transaction_history import TransactionHistory
import constants

from matplotlib import pyplot as plt



#define equities
jupiter_uk_smaller_companies = equity.Equity(name = 'Jupiter UK Smaller Companies I ACC',ISIN='GB00B3LRRF45',provider='yahoo',provider_code='0P0000X1GJ.L',unit = 'GBp')
baillie_american = equity.Equity(ISIN = 'GB0006061963',name = 'Baillie Gifford American B Acc',provider = 'yahoo',provider_code = '0P00000VC9.L',unit = 'GBp')
fidelity_global_tech = equity.Equity(ISIN = 'LU1033663649',name = 'Fidelity Global Technology W Acc',provider = 'investing_com_csv',provider_code = '0P00012CU7',unit = 'GBP')

liontrust_emerging_markets = equity.Equity(name = 'Liontrust Emerging Markets Fund C Acc',provider='yahoo',provider_code='0P0000X63K.L',unit = 'GBp')
legg_mason_japan = equity.Equity(ISIN = 'GB00B8JYLC77',name = 'Legg Mason If Japan Equity X Acc',provider = 'investing_com_csv',provider_code = '0P0000Y692',unit = 'GBP')



#data = baillie_american.get_data(datetime.datetime(2018,2, 1), datetime.datetime(2018,3,1))
history = TransactionHistory();

history.add_cash(20,datetime.datetime(2018,2,1))

history.buy_equity(baillie_american,165.714,datetime.datetime(2018,2, 1))
history.buy_equity(jupiter_uk_smaller_companies,1,datetime.datetime(2018,2, 1));
history.buy_equity(fidelity_global_tech,1,datetime.datetime(2018,2, 1))

#history.sell_equity(baillie_american,700,datetime.datetime(2020,7, 30))
#history.sell_equity(jupiter_uk_smaller_companies,0,datetime.datetime(2020,8, 13))

#portfolio = history.final_portfolio()

portfolio = Portfolio.fromTransactionHistory(history,datetime.datetime(2020,7, 29))


portfolio_value = portfolio.get_holdings_data(datetime.datetime(2018,2, 1), datetime.datetime(2020,2,1))

portfolio_value_percentage_change = analysis_functions.percent_change(portfolio_value)

plt.figure(0)
plt.plot(portfolio_value)
plt.legend(list(portfolio_value.columns))

plt.figure(1)
plt.plot(portfolio_value_percentage_change)
plt.legend(list(portfolio_value_percentage_change.columns))




