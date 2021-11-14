
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os,sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from databases import Databases

from time import sleep

def get_companylist():
    """
    기업리스트 출력
    """
    database = Databases()
    sql = "SELECT DISTINCT symbol FROM usstocklist" #db에 저장된 기업리스트
    curs = database.cursor
    curs.execute(sql) 
    db_stock_list = [item[0] for item in curs.fetchall()] # 기업 symbol리스트
    return db_stock_list


df = get_companylist()
driver = webdriver.Chrome()
for i,ticker in enumerate(df):
    search_key = ticker
    print(i,ticker)
    driver.get('https://m.stock.naver.com/searchItem?searchType=init')
    sleep(0.5)
    elem = driver.find_element_by_class_name("Nbox_input_text")
    elem.send_keys(search_key)
    sleep(0.5)
    selc = driver.find_element_by_id('a_link')
    href = selc.get_attribute('href')
    url = href.replace('total','overview')
    driver.get(url)

    driver.implicitly_wait(3)
    images = driver.find_element_by_xpath('/html/body/div/div[1]/div[4]/div[2]/p[2]')
    print(images.text)
    sleep(1)