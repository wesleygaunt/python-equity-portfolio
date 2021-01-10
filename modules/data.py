# -*- coding: utf-8 -*-
"""
This module creates equities and equity_dicts and populates them with data. 
Only the equities using the yahoo data source will be available on GitHub.
"""
import equity

jupiter_uk_smaller_companies = equity.Equity(name = 'Jupiter UK Smaller Companies I ACC',ISIN='GB00B3LRRF45',provider='morningstar',provider_code='F00000OSWK]2]0]FOGBR$$ALL',unit = 'GBP',equity_type='fund')
legg_mason_japan = equity.Equity(ISIN = 'GB00B8JYLC77',name = 'Legg Mason If Japan Equity X Acc',provider = 'morningstar',provider_code = 'F00000PLVU]2]0]FOGBR$$ALL',unit = 'GBP',equity_type='fund')
baillie_american = equity.Equity(ISIN = 'GB0006061963',name = 'Baillie Gifford American B Acc',provider = 'morningstar',provider_code = 'F0GBR0506U]2]0]FOGBR$$ALL',unit = 'GBP',equity_type='fund')
fidelity_global_tech = equity.Equity(ISIN = 'LU1033663649',name = 'Fidelity Global Technology W Acc',provider = 'morningstar',provider_code = 'F00000SX2A]2]0]FOGBR$$ALL',unit = 'GBP',equity_type='fund')
liontrust_emerging_markets = equity.Equity(name = 'Liontrust Emerging Markets Fund C Acc',ISIN='GB00B8J6SV12',provider='morningstar',provider_code = 'F00000OWFH]2]0]FOGBR$$ALL',unit='GBP',equity_type='fund')
smith_williamson_artificial_intelligence = equity.Equity(ISIN = 'IE00BYPF3314',name = 'Smith & Williamson Artificial Intelligence Z Acc',provider = 'morningstar',provider_code='F00000YYB5]2]0]FOGBR$$AL',unit = 'GBP',equity_type='fund')
marlbourough_us_multicap = equity.Equity(ISIN = 'GB00B906QV32',name = 'Marlborough US Multi-Cap P Inc',provider = 'morningstar',provider_code = 'F00000PBEW]2]0]FOGBR$$ALL',equity_type='fund')

guinness_sustainable_energy = equity.Equity(ISIN = 'IE00BFYV9L73',name = 'Guinness Sustainable Energy Y Acc',provider = 'morningstar',provider_code = 'F0000103JP]2]0]FOGBR$$ALL',equity_type='fund')

hl_special_sit = equity.Equity(name = 'HL Multi-Manager Special Situations Trust M Acc',ISIN = 'GB00BVYV7593', provider='morningstar',provider_code='F00000VDJV]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
lf_lindsell_train_UK = equity.Equity(ISIN = 'GB00BJFLM156', name = 'LF Lindsell Train UK Equity D Acc',provider = 'morningstar',provider_code = 'F00000SS5D]2]0]FOGBR$$ALL',unit = 'GBP', equity_type='fund')
hl_income_growth = equity.Equity(name = 'HL Multi-Manager Income Growth Trust M Acc',ISIN = 'GB00BVYV7601', provider='morningstar',provider_code='F00000VDJW]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
lindsell_train_global = equity.Equity(name = 'Lindsell Train Global Equity D Inc',ISIN = 'IE00BJSPMJ28', provider='morningstar',provider_code='F00000T65V]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
stewart_asia_pacific_leaders = equity.Equity(name = 'Stewart Investors Asia Pacific Leaders Sustainability B Acc',ISIN = 'GB0033874768', provider='morningstar',provider_code='F0GBR04H80]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
stewart_worldwide_equity = equity.Equity(name = 'Stewart Investors Worldwide Equity B Acc',ISIN = 'GB00B4KJBJ07', provider='morningstar',provider_code='F00000MKO3]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
jupiter_india = equity.Equity(name = 'Jupiter India X Acc',ISIN = 'GB00BD08NQ14', provider='morningstar',provider_code='F00000XO3P]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
temple_global_emerging_markets = equity.Equity(name = 'Templeton Global Emerging Markets W Acc',ISIN = 'GB00B7MZ0J00', provider='morningstar',provider_code='F00000OBR5]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
pictet_russian_equities = equity.Equity(name = 'Pictet Russian Equities I' ,ISIN = 'LU0859479239', provider='morningstar',provider_code='F00000PEW2]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
liontrust_european_opportunities = equity.Equity(name = 'Liontrust European Opportunities C Acc' ,ISIN = 'LU0859479239', provider='morningstar',provider_code='F00000OWFI]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
jpmorgan_china = equity.Equity(name = 'JPMorgan China C Acc USD' ,ISIN = 'LU0129472758', provider='morningstar',provider_code='F0GBR05WOZ]2]0]FOGBR$$ALL',unit = 'USD', equity_type = 'fund')
blackrock_world_mining = equity.Equity(name = 'BlackRock Global Funds - World Mining D4' ,ISIN = 'LU0827889725', provider='morningstar',provider_code='F00000OWQG]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
schroder_global_energy = equity.Equity(name = 'Schroder ISF Global Energy A Acc USD' ,ISIN = 'LU0256331488', provider='morningstar',provider_code='F0GBR06U6U]2]0]FOGBR$$ALL',unit = 'USD', equity_type = 'fund')
FSSA_JAPAN_FOCUS = equity.Equity(name = 'FSSA Japan Focus B Hedged Acc' ,ISIN = 'GB00BY9D7B75', provider='morningstar',provider_code='F00000W6RG]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
legg_mason_japan_hedged = equity.Equity(name = 'Legg Mason If Japan Equity X  Hedged Acc' ,ISIN = 'GB00B99C0657', provider='morningstar',provider_code='F00000PW2X]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
artemis_us_smaller_companies = equity.Equity(name = 'Artemis US Smaller Companies I Acc' ,ISIN = 'GB00BMMV5766', provider='morningstar',provider_code='F00000U58R]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')
pictet_robotics = equity.Equity(name = 'Pictet Robotics I Acc' ,ISIN = 'LU1316549283', provider='morningstar',provider_code='F00000WKOC]2]0]FOGBR$$ALL',unit = 'GBP', equity_type = 'fund')

ceres = equity.Equity(name = 'Ceres Power Holdings PLC',ISIN = 'GB00BG5KQW09',provider = 'morningstar',provider_code='0P00007YQ0]3]0]E0WWE$$ALL',unit = 'GBP',equity_type='stock')

#yahoo data funds - provided as examples 
astrazeneca = equity.Equity(name = 'astrazeneca plc',provider='yahoo',provider_code='AZN.L',unit = 'GBp',symbol = 'AZN.L',equity_type='stock')
shell = equity.Equity(name = 'Royal Dutch Shell plc',provider='yahoo',provider_code='RDSB.L',unit = 'GBp',symbol = 'RDSB.L',equity_type='stock')
tesco = equity.Equity(name = 'tesco plc',provider='yahoo',provider_code='TSCO.L',unit = 'GBp',symbol = 'TSCO.L',equity_type='stock')
rightmove = equity.Equity(name = 'rightmove plc',provider='yahoo',provider_code='RMV.L',unit = 'GBp',symbol = 'RMV.L',equity_type='stock')


globals_dict = globals().copy()

all_equities = equity.EquityDict()
for key in globals_dict:
    item = globals_dict[key]
    if(type(item) == equity.Equity):
        all_equities.add_equity(item)
        #item.save_equity()
del globals_dict   

funds = equity.EquityDict()
for key in all_equities:
    eq = all_equities[key]
    if(eq.equity_type == 'fund'):  
        funds.add_equity(eq)    

stocks = equity.EquityDict()
for key in all_equities:
    eq = all_equities[key]
    if(eq.equity_type == 'stock'):  
        stocks.add_equity(eq)    

del eq

#contains        
HL_equities = {
    'JUPITER_UK_SMALLER_COMPANIES_CLASS_I_ACCUMULATION_(GBP)':jupiter_uk_smaller_companies,
    'LIONTRUST_EMERGING_MARKETS_CLASS_C_ACCUMULATION_(GBP)':liontrust_emerging_markets,
    'LEGG_MASON_IF_JAPAN_EQUITY_CLASS_X_ACCUMULATION_(GBP)':legg_mason_japan,
    'BAILLIE_GIFFORD_AMERICAN_CLASS_B_ACCUMULATION_(GBP)':baillie_american,
    'SMITH_&_WILLIAMSON_ARTIFICIAL_INTELLIGENCE_CLASS_Z_ACCUMULATION_(GBP)':smith_williamson_artificial_intelligence,
    'FIDELITY_GLOBAL_TECHNOLOGY_CLASS_W_ACCUMULATION_(GBP)':fidelity_global_tech,
    'MARLBOROUGH_US_MULTI_CAP_INCOME_CLASS_P_INCOME_(GBP)':marlbourough_us_multicap,
    'CERES_POWER_HOLDINGS_ORD_GBP0.10':ceres,

    'HL_MULTI_MANAGER_SPECIAL_SITUATIONS_TRUST_CLASS_M_ACCUMULATION_(GBP)':hl_special_sit,
    'LF_LINDSELL_TRAIN_UK_EQUITY_CLASS_D_ACCUMULATION_(GBP)':lf_lindsell_train_UK,
    'HL_MULTI_MANAGER_INCOME_&_GROWTH_TRUST_CLASS_M_ACCUMULATION_(GBP)':hl_income_growth,
    'LINDSELL_TRAIN_GLOBAL_EQUITY_CLASS_D_INCOME_(GBP)':lindsell_train_global,
    'STEWART_INV_ASIA_PACIFIC_LEADERS_SUSTAINABILITY_CLASS_B_ACCUMULATION_(GBP)':stewart_asia_pacific_leaders,
    'STEWART_INVESTORS_WORLDWIDE_EQUITY_CLASS_B_ACCUMULATION_(GBP)':stewart_worldwide_equity,
    'SCHRODER_ISF_GLOBAL_ENERGY_INCLUSIVE_CLASS_A_ACCUMULATION_(USD)':schroder_global_energy,
    'JUPITER_INDIA_CLASS_X_ACCUMULATION_(GBP)':jupiter_india,
    'TEMPLETON_GLOBAL_EMERGING_MARKETS_CLASS_W_ACCUMULATION_(GBP)':temple_global_emerging_markets,
    'PICTET_RUSSIAN_EQUITIES_CLASS_I_ACCUMULATION_(GBP)':pictet_russian_equities,
    'LIONTRUST_EUROPEAN_OPPORTUNITIES_CLASS_C_ACCUMULATION_(GBP)':liontrust_european_opportunities,
    'JPMORGAN_CHINA_CLASS_C_ACCUMULATION_(USD)':jpmorgan_china,
    'BLACKROCK_WORLD_MINING_CLASS_D4_INCOME_(GBP)':blackrock_world_mining,
    'FSSA_JAPAN_FOCUS_HEDGED_CLASS_B_ACCUMULATION_(HEDGED_GBP)':FSSA_JAPAN_FOCUS,
    'LEGG_MASON_IF_JAPAN_EQUITY_CLASS_X_ACCUMULATION_(HEDGED_GBP)':legg_mason_japan_hedged,
    'ARTEMIS_US_SMALLER_COMPANIES_CLASS_I_ACCUMULATION_(GBP)':artemis_us_smaller_companies,
    'PICTET_ROBOTICS_CLASS_I_ACCUMULATION_(GBP)':pictet_robotics,
    'GUINNESS_SUSTAINABLE_ENERGY_CLASS_Y_ACCUMULATION_(GBP)':guinness_sustainable_energy
}