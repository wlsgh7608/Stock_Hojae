
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from ..databases import Databases
from time import sleep

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


df = get_companylist()
driver = webdriver.Chrome()
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

    driver.get(url)
    driver.implicitly_wait(3)
    images = driver.find_element_by_class_name('.OverviewContainer_desc__unQ18')
    print(images)

    sleep(2)