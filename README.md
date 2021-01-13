# python-equity-portfolio
## Introduction
A simple portfolio tracker that was orignally built with the purpose of tracking Hargreaves Lansdown stocks and shares portfolios. It has now grown into a more fully fledged share and mutual fund historical price tracking package, porfolio tracker and fund creation/tracking functionality, with various interlinked modules. 

Features include:
* [Hargreaves Lansdown](hl.co.uk/) transaction history import funtionality.
* Plot current porfolios, historical portfolios and annual performance of stocks, ETFs and mutual funds.
* Full transaction history performance *and* historical portfolio creation from transaction data.
* Historical share/fund price requests from yahoo finance, investing.com and others. 
* Stock bundling: Allows bundling of shares to add to a portfolio as a fund which can be placed into portfolios together. 

## Usage

[Examples](https://github.com/wesleygaunt/python-equity-portfolio/blob/main/examples) contains 3 basic examples which introduces the equity, portfolio and transaction classes and can be run without any extra data. The transaction history can be manually populated or the HL data importer can be used to create transaction data.

[hl_import_example.py](https://github.com/wesleygaunt/python-equity-portfolio/blob/main/examples/hl_import_example.py) requires a HL transaction *csv* file, which is available from your transaction history tab on the HL website. 

## Notes on the data sources
When I started work on the project, the data for historical fund and share prices all came from [yahoo finance](https://uk.finance.yahoo.com/) which has the ability to export historical data as a csv file (see [data_requests.py](https://github.com/wesleygaunt/python-equity-portfolio/blob/main/modules/data_requests.py)). However, later on I found a method to request data from the morningstar website, however - as I'm dubious of the legality of this (they do have a pay-to-use API available) I have not published the method with which this was done. Therefore the funtionality of the code is crippled. 

## Dependancies 
The project was written in python 3.7.3 and requires the following modules:

'''python
datetime
bokeh
pandas
itertools 
calendar
warnings
io
requests
json
numpy
'''
