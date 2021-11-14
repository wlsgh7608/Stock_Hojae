from rest_framework.response import Response
from django.shortcuts import render
from django.http.response import HttpResponse
import FinanceDataReader as fdr

from stock.serializers import CurrentStockSerializer
from .models import CurrentStock, UsCompanyDaily,UsStocklist,Stockdesc
import pandas as pd
import datetime
from rest_framework.decorators import api_view
from time import sleep
from rest_framework.generics import ListAPIView

# crawling
import os,sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your views here.

class currentStocklist(ListAPIView):
    """
    최신날짜 주식정보 출력
    """
    queryset = CurrentStock.objects.all()
    serializer_class = CurrentStockSerializer


def current_stock_update(symbol,company_data,close,open,high,low,volume,change,date):
    isexist = CurrentStock.objects.filter(symbol = symbol)
    if isexist:
        # 존재할시 update
        print("exist")
        current_stock = CurrentStock.objects.get(symbol = company_data)
        current_stock.close = close
        current_stock.open = open
        current_stock.high = high
        current_stock.low = low
        current_stock.volume = volume
        current_stock.change = change
        current_stock.date = date
        current_stock.save()
    else:
        print("does not exist")
        # 존재하지 않을 시 create
        CurrentStock.objects.create(symbol = company_data,
        close = close,
        open = open,
        high = high,
        low = low,
        volume = volume,
        change = change,
        date = date)

def stock_update(symbol_data):
    symbol = symbol_data.symbol
    query_symbol = symbol.replace('.','') # 티커명 investing.com 맞게 변경

    current_date = UsCompanyDaily.objects.filter(company_code = symbol_data).first().stock_date
    next_date = current_date+datetime.timedelta(days= 1)

    stock_data = fdr.DataReader(query_symbol,next_date) # 다음날부터 update
    for j,row in enumerate(stock_data.itertuples()):
        date,close,open,  high , low, volume,change  = row # unpacking
        volume = int(volume)
        change = round(change,5)
        UsCompanyDaily.objects.create(company_code = symbol_data,stock_date= date,
        close=close,open=open,high=high,low=low,volume=volume,change=change)
        if j == len(stock_data)-1:
            current_stock_update(symbol,symbol_data,close,open,high,low,volume,change,date) # 최신 주가로 업데이트




@api_view(['GET'])
def individual_stock_update(self,symbol):
    company = UsStocklist.objects.filter(symbol = symbol)
    if company:
        company_data = company.get(symbol = symbol)
        stock_update(company_data)
        return Response({"message":"create success"},status = 200)


@api_view(['GET'])
def entire_stock_update(request):
    company_list = UsStocklist.objects.all()
    for i,company in enumerate(company_list):
        if i>= 80:
            print(i,company,"update")
            stock_update(company)
            sleep(3)
    return Response({"message":"entire update success"},status = 200)


@api_view(['GET'])
def entire_stock_desc(request):
    objects = UsStocklist.objects.all()
    driver = webdriver.Chrome('C:/Users/Jinho/DjangoProjects/hojae/stock/chromedriver.exe')
    for i,object in enumerate(objects):

        ticker = object.symbol
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
        desc = images.text
        print(len(desc))
        symbol = UsStocklist.objects.get(symbol = ticker)
        Stockdesc.objects.create(symbol = symbol,description = desc)

        sleep(1)
    return Response({"message":"entire description success"},status = 200)




# def stockUpdate(request,)