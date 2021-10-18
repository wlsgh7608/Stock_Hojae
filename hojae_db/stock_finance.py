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

def _parse_json(url, headers = {'User-agent': 'Mozilla/5.0'}):
    html = requests.get(url=url, headers = headers).text

    json_str = html.split('root.App.main =')[1].split(
        '(this)')[0].split(';\n}')[0].strip()
    
    try:
        data = json.loads(json_str)[
            'context']['dispatcher']['stores']['QuoteSummaryStore']
    except:
        return '{}'
    else:
        # return data
        new_data = json.dumps(data).replace('{}', 'null')
        new_data = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)

        json_info = json.loads(new_data)

        return json_info


aapl = get_data('aapl')
AAPL  = si.get_income_statement('msft',yearly=True)

# si._parse_json

ticker = 'SONY'
income_site = "https://finance.yahoo.com/quote/" + ticker + \
            "/financials?p=" + ticker

json_info = _parse_json(income_site)
# print(json_info)
# print(json_info["earnings"]['financialCurrency'])
# column = ['totalRevenue','grossProfit','operatingIncome','netIncome']

# # print(AAPL.loc[column,:])
# df =AAPL.loc[column,:]
# print(fdr.DataReader('USD/KRW','today'))
print(fdr.DataReader('JPY/USD','today')['Close'])
print(fdr.DataReader('JPY/USD','today')['Close']*0.001)
# print(float(fdr.DataReader('TWD/USD','today')['Close']))
# query_symbol='SONY'
# df = si.get_income_statement(query_symbol,yearly=True)
# print(df)

# print(df)




# print(AAPL.shape)