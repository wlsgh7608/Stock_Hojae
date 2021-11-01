from yahoo_fin.stock_info import get_data, tickers_sp500, tickers_nasdaq, tickers_other
import yahoo_fin.stock_info as si
import pandas as pd

from crud import CRUD
from databases import Databases
from time import sleep
import FinanceDataReader as fdr
import requests
import pandas as pd
import ftplib
import io
import re
import json
import datetime

CURRENCY_LIST = {
    'KRW':fdr.DataReader('KRW/USD','today')['Close'],
    'JPY':fdr.DataReader('JPY/USD','today')['Close']*0.01, #환율값 오류인듯
    'CNY':fdr.DataReader('CNY/USD','today')['Close'],
    'EUR':fdr.DataReader('EUR/USD','today')['Close'],
    'TWD':fdr.DataReader('TWD/USD','today')['Close']
    }

def get_today_currency(currency):
    """ 환율 계산"""
    if currency == 'USD':
        return 0.001
    elif currency in CURRENCY_LIST:
        return CURRENCY_LIST.get(currency)*0.001
    else:
        return fdr.DataReader(str(currency)+'/USD','today')['Close']*0.001



df = si.get_balance_sheet('DXCM') 
df = df.loc[['totalLiab','totalStockholderEquity','totalAssets','totalCurrentAssets','totalCurrentLiabilities'],:]
symbol = 'DXCM'


income_site = "https://finance.yahoo.com/quote/" + symbol + \
            "/balance-sheet?p=" + symbol
json_info = si._parse_json(income_site)
try:
    currency = json_info["earnings"]['financialCurrency'] # 통화 parsing
    print("currency",currency)
except:
    print("not exist")
    currency = 'USD'
multiple = float(get_today_currency(currency))
print('multiple : ',multiple)
df =df.mul(multiple).transpose()

print(df)
# print(AAPL.shape)