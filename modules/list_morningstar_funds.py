import pandas as pd

def request_morningstar_funds():
    url = ("https://tools.morningstar.co.uk/api/rest.svc/klr5zyak8x/security/"
           + "screener?"
           + "page=1"
           + "&pageSize=10000"
           + "&sortOrder=LegalName%20asc"
           + "&outputType=json"
           + "&version=1"
           + "&languageId=en-GB"
           + "&currencyId=GBP"
           + "&universeIds=FOGBR%24%24ALL"
           + "&securityDataPoints="
           + "SecId|"
           + "Name|"
           + "PriceCurrency|"
           + "TenforeId|"
           + "LegalName|"
           + "ClosePrice|"
           + "StarRatingM255|"
           + "SustainabilityRank|"
           + "QuantitativeRating|"
           + "AnalystRatingScale|"
           + "CategoryName|"
           # + "Yield_M12|"
           # + "GBRReturnD1|"
           # + "GBRReturnW1|"
           # + "GBRReturnM1|"
           # + "GBRReturnM3|"
           # + "GBRReturnM6|"
           # + "GBRReturnM0|"
           # + "GBRReturnM12|"
           # + "GBRReturnM36|"
           # + "GBRReturnM60|"
           # + "GBRReturnM120|"
           # + "MaxFrontEndLoad|"
           # + "OngoingCostActual|"
           # + "PerformanceFeeActual|"
           # + "TransactionFeeActual|"
           # + "MaximumExitCostAcquired|"
           # + "FeeLevel|"
           # + "ManagerTenure|"
           # + "MaxDeferredLoad|"
           # + "InitialPurchase|"
           # + "FundTNAV|"
           # + "EquityStyleBox|"
           # + "BondStyleBox|"
           # + "AverageMarketCapital|"
           # + "AverageCreditQualityCode|"
           # + "EffectiveDuration|"
           # + "MorningstarRiskM255|"
           # + "AlphaM36|"
           # + "BetaM36|"
           # + "R2M36|"
           # + "StandardDeviationM36|"
           # + "SharpeM36|"
           # + "InvestorTypeRetail|"
           # + "InvestorTypeProfessional|"
           # + "InvestorTypeEligibleCounterparty|"
           # + "ExpertiseBasic|"
           # + "ExpertiseAdvanced|"
           # + "ExpertiseInformed|"
           # + "ReturnProfilePreservation|"
           # + "ReturnProfileGrowth|"
           # + "ReturnProfileIncome|"
           # + "ReturnProfileHedging|"
           # + "ReturnProfileOther|"
           # + "TrackRecordExtension"
           + "&filters="
           + "&term="
           + "&subUniverseId=")
    
    df = pd.read_json(url)
    total = df.iloc[0]['total']
    print(total)
    
    data_list = list(df['rows'])
    
    
    
    df = pd.DataFrame(data_list)    
    

    
    return df
