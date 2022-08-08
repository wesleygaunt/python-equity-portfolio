import pandas as pd


def request_morningstar_funds(page = 1, pageSize = 10, universeId = "FOGBR$$ALL"):
    url = ("https://tools.morningstar.co.uk/api/rest.svc/klr5zyak8x/security/"
           + "screener?"
           + "page=" + str(page)
           + "&pageSize=" + str(pageSize)
           + "&sortOrder=LegalName%20asc"
           + "&outputType=json"
           + "&version=1"
           + "&languageId=en-GB"
           + "&currencyId=GBP"
           + "&universeIds=" + universeId
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
    data_list = list(df['rows'])
    df = pd.DataFrame(data_list)    
    

    
    return total, df

def list_funds(universeId = "FOGBR$$ALL", pageSize = 10000):
    total, df = request_morningstar_funds(page = 1, pageSize = 1)
    print(total)
    
    remaining_funds = total
    page = 1
    
    pages = []
    while(remaining_funds > 0):
        print("Page = " + str(page))
        print("Remaining funds = " + str(remaining_funds))
        print("*********************************\n\n\n\n")
        
        total, current_page = request_morningstar_funds(page = page, pageSize = pageSize)
        page = page + 1
        remaining_funds = remaining_funds - pageSize
        pages.append(current_page)
        
        
    df = pd.concat(pages, ignore_index = True)
    
    return df
#df = list_funds()

def save_to_JSON(dataframe, path):
    dataframe.to_json(path + '/data.json')
def load_from_JSON(path):
    dataframe = pd.read_json(path + '/data.json')
    return dataframe
#df = request_morningstar_funds(page = 2,pageSize = 50000)