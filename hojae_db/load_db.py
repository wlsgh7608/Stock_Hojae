import enum
import FinanceDataReader as fdr
import psycopg2
import pandas as pd
import datetime
import db_id
from crud import CRUD
from databases import Databases
from time import sleep
import yahoo_fin.stock_info as si


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

                # db.insertDB(schema='public',table='stock_uscompanydaily',column=column,data=data)
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
        if i>=147:

            symbol = db_stock_list[i]
            query_symbol = symbol.replace('.','-')
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



       



    AAPL  = si.get_income_statement('AAPL',yearly=True)

def drop_us_stocklist():
    df_amex = fdr.StockListing('AMEX')
    conn = psycopg2.connect(host='192.168.55.107', dbname='hojae',user='postgres',password='wlsgh7608',port=5432)
    # database = Databases()

    
    # print(database.execute('SELECT symbol FROM us_stocklist;'))
    # database.commit

    # db = CRUD()
    for i,row in enumerate(df_amex.itertuples()):

        _,symbol,  name , industry, industry_id  = row # unpacking
        cursor = conn.cursor()
        print(cursor.execute(f"select * from us_stocklist where symbol = 'NML';"))
        # print(cursor.execute(f"SELECT * from us_stocklist where symbol = '{symbol}';"))
        # cursor.execute(f"DELETE from us_stocklist where symbol = '{symbol}';")
        # database.commit()
        # cunn.close()
    #     table = 'us_stocklist'
    #     condition = f"symbol = '{symbol}'"
    #     db.deleteDB(schema= 'public',table = table,condition = condition)
        

    


if __name__ == '__main__':
    # create_table_us_stocklist()
    # create_table_us_stockinfo()
    # create_us_stocklist()
    # create_us_stockinfo()
    # drop_us_stocklist()
    create_us_incomestatement()
    