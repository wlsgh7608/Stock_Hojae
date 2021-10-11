import enum
import FinanceDataReader as fdr
import psycopg2
import pandas as pd
import datetime
import db_id
from crud import CRUD
from databases import Databases
from time import sleep



def create_table_us_stocklist():

    """ 미국주식 상장리스트 DB table 생성 """
        
    commands = (
        """
        CREATE TABLE us_stocklist(
            symbol VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            industry VARCHAR(50) NOT NULL,
            industry_id INTEGER NOT NULL,
        )""",
        
    )
    conn = psycopg2.connect(host = 'localhost',dbname = 'hojae',user= 'postgres',password = 'wlsgh7608',port = '5432')
    cur = conn.cursor()
    for command in commands:
        print(command)
        cur.execute(command)
        conn.commit()
def create_table_us_stockinfo():
    commands = (
        """
        CREATE TABLE us_stocklist(
            symbol VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            industry VARCHAR(50) NOT NULL,
            industry_id INTEGER NOT NULL,
        )""",
        
    )

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
                s_date,close,open,  high , low, volume,change  = row # unpacking
                s_date = s_date.strftime("%y-%m-%d")
                volume = int(volume)
                change = round(change,5)
                column = "company_code_id,stock_date,close,open,high,low,volume,change"
                data = c_name,s_date,close,open,high,low,volume,change

                db.insertDB(schema='public',table='stock_uscompanydaily',column=column,data=data)
        sleep(5)
            

                    

            

            # print(symbol_data)
        
    

    





def create_us_stocklist():
    """
    나스닥,뉴욕,아멕스 각 시가총액기준 상위 100개 기업(total : 300) db에 업데이트
    """
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(today)
    data = db_id.db_identification()
    df_nasdaq= fdr.StockListing('NASDAQ')[:100]
    df_nyse = fdr.StockListing('NYSE') [:100]
    df_amex = fdr.StockListing('AMEX')[:100]
    df = pd.concat([df_nasdaq,df_nyse,df_amex])
    # df = df_nasdaq
    insertsql = """insert into us_stocklist (symbol, name, industry, industry_id) values (%s, %s, %s, %d),"""

    db = CRUD()

    for i,row in enumerate(df.itertuples()):
        _,symbol,  name , industry, industry_id  = row # unpacking
    
        table = "us_stocklist"
        column = "symbol,name,industry,industry_id"
        name= name.replace("\'"," ")
        data = symbol,name,industry,int(industry_id)
        db.insertDB(schema='public',table='us_stocklist',column=column,data=data)
    


# for i,ticker in enumerate(df):
    # print(ticker)

if __name__ == '__main__':
#    create_us_stockinfo()
    print(fdr.DataReader('TSLA','2010'))