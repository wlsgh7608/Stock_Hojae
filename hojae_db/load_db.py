import FinanceDataReader as fdr
import psycopg2
import pandas as pd
import datetime
import db_id
from crud import CRUD
from databases import Databases
from time import sleep
import yahoo_fin.stock_info as si
import requests
from bs4 import BeautifulSoup

CURRENCY_LIST = {
    'KRW':fdr.DataReader('KRW/USD','today')['Close'],
    'JPY':fdr.DataReader('JPY/USD','today')['Close']*0.01, #환율값 오류
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

def create_table_us_stocklist():

    """ 미국주식 상장리스트 DB table 생성 """
        
    commands = (
        """
        CREATE TABLE us_stocklist(
            symbol VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            industry VARCHAR(50) NOT NULL,
            industry_id INTEGER NOT NULL
        )""",
        
    )
    conn = psycopg2.connect(host = '192.168.55.107',dbname = 'hojae',user= 'postgres',password = 'wlsgh7608',port = '5432')
    cur = conn.cursor()
    for command in commands:
        print(command)
        cur.execute(command)
        conn.commit()
        

def create_us_stockinfo():
    """
    기업별 주식 정보 symbol, 기업이름, 시가,종가,거래량,상승률 2010년~ 크롤링
    """
    database = Databases()

    sql = "SELECT DISTINCT symbol FROM us_stocklist" 
    curs = database.cursor
    curs.execute(sql) 
    db_stock_list = [item[0] for item in curs.fetchall()]
    db = CRUD()
    for i,c_name in enumerate(db_stock_list):
        print(i,c_name)
        symbol = db_stock_list[i]
        symbol = symbol.replace('.','')
        ifexist = f"SELECT count(*) from stock_uscompanydaily where company_code_id = '{c_name}';"
        if c_name == "UN":
            continue
        result_ifexist = database.execute(ifexist)
        cnt = result_ifexist[0][0]
        if cnt>0:
                print(i,c_name,"exists")
                continue
        else:
            symbol_data = fdr.DataReader(symbol,'2010') # 2010년부터 일일데이터 로드
            for j,row in enumerate(symbol_data.itertuples()):
                print(row)
                s_date,close,open,  high , low, volume,change  = row # unpacking
                s_date = s_date.strftime("%y-%m-%d")
                volume = int(volume)
                change = round(change,5)
                column = "company_code_id,stock_date,close,open,high,low,volume,change"
                data = c_name,s_date,close,open,high,low,volume,change
                db.insertDB(schema='public',table='stock_uscompanydaily',column=column,data=data)
        sleep(5)

def create_us_stocklist():
    """
    나스닥,뉴욕 각 100개 기업(total : 200) db에 업데이트
    """
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(today)
    data = db_id.db_identification()
    df_nasdaq= fdr.StockListing('NASDAQ')[:100]
    df_nyse = fdr.StockListing('NYSE') [:100]
    df = pd.concat([df_nasdaq,df_nyse])
    insertsql = """insert into us_stocklist (symbol, name, industry, industry_id) values (%s, %s, %s, %d),"""

    db = CRUD()

    for i,row in enumerate(df.itertuples()):
        _,symbol,  name , industry, industry_id  = row # unpacking
    
        table = "us_stocklist"
        column = "symbol,name,industry,industry_id"
        name= name.replace("\'"," ")
        data = symbol,name,industry,int(industry_id)
        db.insertDB(schema='public',table='us_stocklist',column=column,data=data)
def create_us_incomestatement():
    """
    기업 손익계산서
    """    
    database = Databases()

    sql = "SELECT DISTINCT symbol FROM us_stocklist" #db에 저장된 기업리스트
    curs = database.cursor
    curs.execute(sql) 
    db_stock_list = [item[0] for item in curs.fetchall()] # 기업 symbol리스트
    db = CRUD()

    for i,symbol in enumerate(db_stock_list):
        print(i,symbol)
        symbol = db_stock_list[i]
        query_symbol = symbol.replace('.','-') # 티커명 yahoofinance에 맞게 변경
        df = si.get_income_statement(query_symbol,yearly=True)

        income_site = "https://finance.yahoo.com/quote/" + symbol + \
            "/financials?p=" + symbol
        json_info = si._parse_json(income_site)
        try:
            currency = json_info["earnings"]['financialCurrency'] # 통화 parsing
        except:
            currency = 'USD'
        multiple = float(get_today_currency(currency))
        print('multiple : ',multiple)
        df =df.mul(multiple)
        column = ['totalRevenue','grossProfit','operatingIncome','netIncome']
        df =df.loc[column,:].transpose()
        
        for j,row in enumerate(df.itertuples()):
                _,totalRevenue,grossProfit,  operatingIncome , netIncome = row # unpacking
                e_date = df.index[j]
                e_date = e_date.strftime("%y-%m-%d")
                column = "end_date,revenue,gross_profit,operating_income,net_income,company_code_id"
                #정수범위때문에 전처리
                totalRevenue,grossProfit,operatingIncome,netIncome= int(totalRevenue),int(grossProfit),int(operatingIncome),int(netIncome)
                data = e_date,totalRevenue,grossProfit,  operatingIncome , netIncome,symbol
                print(data)
                db.insertDB(schema='public',table='incomestatement',column=column,data=data)
        sleep(2)
def get_companylist():
    """
    기업리스트 출력
    """
    database = Databases()
    sql = "SELECT DISTINCT symbol FROM us_stocklist" #db에 저장된 기업리스트
    curs = database.cursor
    curs.execute(sql) 
    db_stock_list = [item[0] for item in curs.fetchall()] # 기업 symbol리스트
    return db_stock_list


def company_description():
    """
    기업 설명
    """
    df = get_companylist()
    print(df)

    for i,ticker in enumerate(df):
        print(i,ticker)
        url = "http://m.stock.naver.com/index.html#/worldstock/stock/"+ticker+".O/overview"
        if '.' in ticker:
            print("yes",ticker)
            a,b = ticker.split('.')
            b = b.lower()
            print(a,b)
            ticker = a+b
            url = "http://m.stock.naver.com/index.html#/worldstock/stock/"+ticker+"/overview"
        print(url)
        header = {'User-Agent' : 'Mozilla/5.0'}
        webpage = requests.get(url,headers=header)
        soup = BeautifulSoup(webpage.content, "html.parser")
        content = soup.select('#content > div.OverviewContainer_overviewContainer__2Gzn5 > div.OverviewContainer_infoCorp__3K5qX > p.OverviewContainer_desc__unQ18')
        print(soup)

        sleep(2)

    
    

def create_us_balancesheet():
    """
    기업 대차대조표
    """    
    database = Databases()

    sql = "SELECT DISTINCT symbol FROM us_stocklist" #db에 저장된 기업리스트
    curs = database.cursor
    curs.execute(sql) 
    db_stock_list = [item[0] for item in curs.fetchall()] # 기업 symbol리스트
    db = CRUD()

    for i,symbol in enumerate(db_stock_list):
        if i>= 89:
            print(i,symbol)
            symbol = db_stock_list[i]
            query_symbol = symbol.replace('.','-') # 티커명 yahoofinance에 맞게 변경
            df = si.get_balance_sheet(query_symbol,yearly=True)

            income_site = "https://finance.yahoo.com/quote/" + symbol + \
                "/balance-sheet?p=" + symbol
            json_info = si._parse_json(income_site)
            try:
                currency = json_info["earnings"]['financialCurrency'] # 통화 parsing
            except:
                print("currency not exist. So default USD")
                currency = 'USD'
            multiple = float(get_today_currency(currency))
            print('multiple : ',multiple)
            df =df.mul(multiple)
            column = ['totalLiab','totalStockholderEquity','totalAssets','totalCurrentAssets','totalCurrentLiabilities']
            df = df.loc[column,:]
            df = df.dropna(axis=1)
            print(df)
            df =df.transpose()
            
            for j,row in enumerate(df.itertuples()):
                    _,totalLiab,totalStockholderEquity,  totalAssets , totalCurrentAssets ,totalCurrentLiabilities= row # unpacking
                    e_date = df.index[j]
                    e_date = e_date.strftime("%y-%m-%d")
                    column = "end_date,total_liability,total_stockholder_equity,total_assets,total_current_assets,total_current_liability,company_code_id"
                    #정수범위때문에 전처리
                    totalLiab,totalStockholderEquity,totalAssets,= int(totalLiab),int(totalStockholderEquity),int(totalAssets)
                    totalCurrentAssets,totalCurrentLiabilities = int(totalCurrentAssets),int(totalCurrentLiabilities)
                    data = e_date,totalLiab,totalStockholderEquity,  totalAssets , totalCurrentAssets,totalCurrentLiabilities,symbol
                    print(data)
                    db.insertDB(schema='public',table='balancesheet',column=column,data=data)
            sleep(2)
    
def news_us():
    ticker = 'MSFT'
    url = "https://www.stockwatch.com/Quote/Detail?U:" + ticker
    print("urL",url)
    source_code = requests.get(url).text
    html = BeautifulSoup(source_code,'lxml')
    print(source_code)

    
    # links = html.select('#MainContent_NewsList1_Table1_Table1 > tbody')
    #news link
    # print(links)
    # news_list = links.find_all('a')
    # link_list = []
    # for i,news in enumerate(news_list):
    #     if i%2 ==1:
    #          link = news.attrs['href']
    #          news_link = 'https://www.stockwatch.com/'+link
    #          print(news_link)
    #          link_list.append(news_link)
    # return link_list

def update():
    # print(fdr.DataReader("TSLA",'2021-10-20'))
    print(fdr.DataReader('TSLA'))

if __name__ == '__main__':
    create_table_us_stocklist()
    create_table_us_stockinfo()
    create_us_stocklist()
    create_us_stockinfo()
    create_us_balancesheet()
    company_description()
    news_us()
    update()