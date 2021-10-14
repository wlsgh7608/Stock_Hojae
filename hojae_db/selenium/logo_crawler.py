from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request 
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from databases import Databases


"""
기업들의 로고 크롤링
"""

driver = webdriver.Chrome()
driver.get("https://www.google.co.kr/search?q=google&tbm=isch&ved=2ahUKEwi-4ujFm8nzAhUCMKYKHT80DbMQ2-cCegQIABAA&oq=google&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyBQgAEIAEMggIABCABBCxAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMggIABCABBCxAzIFCAAQgAQ6CwgAEIAEELEDEIMBUIo6WII_YL0_aABwAHgAgAF8iAHbBJIBAzAuNZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=PsZnYb7LKoLgmAW_6LSYCw&authuser=0&bih=875&biw=1036&hl=ko")
image_folder = "C:/Users/Jinho/DjangoProjects/hojae/hojae_db/company_logo/"
database  = Databases()
sql = "SELECT DISTINCT symbol,name FROM us_stocklist"
curs = database.cursor
curs.execute(sql)
company_list = [[item[0],item[1]] for item in curs.fetchall()] # US_stocklist의 symbol, name을 저장

for p,(symbol,cname) in enumerate(company_list):
    if p>= 100:

        print(p,symbol,cname)
        search_key = cname+' logo'
        elem = driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys(search_key)
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        images = driver.find_elements_by_css_selector('.rg_i.Q4LuWd')
        count = 1
        for image in images:
            if count>3:
                break
            image.click()
            time.sleep(1)
            try:
                imgUrl = driver.find_element_by_css_selector('.n3VNCb').get_attribute('src')
                urllib.request.urlretrieve(imgUrl,image_folder+symbol+"_"+str(count)+'.jpg')
                count+=1
            except Exception  as e:
                print(e)
                print(p,symbol,cname, "오류발생")
                continue

assert "No results found." not in driver.page_source
driver.close()


