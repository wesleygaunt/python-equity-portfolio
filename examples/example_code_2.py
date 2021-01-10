# -*- coding: utf-8 -*-
"""
Example 2:
    Demonstates the use of the portfolio module, and the fund module which inherits from it.
"""
import datetime

#my modules
import analysis_functions
import equity
import portfolio
import plot

#define equities
baillie_american = equity.Equity(ISIN = 'GB0006061963',name = 'Baillie Gifford American B Acc yahoo',provider = 'yahoo',provider_code = '0P00000VC9.L',unit = 'GBp')
jupiter_uk_smaller_companies = equity.Equity(name = 'Jupiter UK Smaller Companies I ACC yahoo',ISIN='GB00B3LRRF45',provider='yahoo',provider_code='0P0000X1GJ.L',unit = 'GBp')

pf = portfolio.Portfolio()


pf[baillie_american] = 100
pf[jupiter_uk_smaller_companies] = 200
pf.change_cash(1000)

start_date = datetime.datetime(2020,1, 1)
end_date = datetime.datetime(2021,1,1)

pf_value = pf.get_holdings_data(start_date, end_date)

pf_percentage_change = analysis_functions.percent_change(pf_value)

plot.line(pf_value,axis = 'value',title = 'Portfolio Value')
plot.line(pf_percentage_change,axis = 'percentage', title = 'Percentage Change')
