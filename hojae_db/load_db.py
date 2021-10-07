import FinanceDataReader as fdr
import psycopg2
import pandas as pd
import datetime
import db_id
from crud import CRUD



def create_us_stocklist():

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


today = datetime.datetime.now().strftime('%Y-%m-%d')
print(today)

data = db_id.db_identification()


df_nasdaq= fdr.StockListing('NASDAQ')[:100]
df_nyse = fdr.StockListing('NYSE') [:100]
df_amex = fdr.StockListing('AMEX')[:100]


df = pd.concat([df_nasdaq,df_nyse,df_amex])
# df = df_nasdaq
insertsql = """insert into us_stocklist (symbol, name, industry, industry_id) values (%s, %s, %s, %d),"""
conn = psycopg2.connect(host = 'localhost',dbname = 'hojae',user= 'postgres',password = 'wlsgh7608',port = '5432')

db = CRUD()

# example = "INSERT INTO us_stocklist ("
for i,row in enumerate(df.itertuples()):
    _,symbol,  name , industry, industry_id  = row # unpacking
   
    table = "us_stocklist"
    column = "symbol,name,industry,industry_id"
    name= name.replace("\'"," ")

    # print(column)
    data = symbol,name,industry,int(industry_id)

    # insertsql = " INSERT INTO  {table}({column}) values {data};".format(table=table,column=column,data=data)
    db.insertDB(schema='public',table='us_stocklist',column=column,data=data)
    

# for i,ticker in enumerate(df):
    # print(ticker)

# if __name__ == '__main__':
#     create_us_stocklist()