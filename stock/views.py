from django.db import reset_queries
from django.db.models import query
from rest_framework import generics, serializers
from rest_framework.response import Response
from django.shortcuts import render
from django.http.response import HttpResponse
import FinanceDataReader as fdr
from rest_framework.views import APIView

from stock.serializers import BalanceSheetSerializer, CurrentStockSerializer, StockDescSerialzier,StockPageEntireSerializer, UsStockListSerializer,NewsContentsSerializer
from .models import BalanceSheet, CurrentStock, Newscontents, StockAdditional, UsCompanyDaily,UsStocklist,Stockdesc
import pandas as pd
import datetime
from rest_framework.decorators import api_view
from time import sleep
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
import requests, json
# crawling
import os,sys
# from datetime import datetime
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
        if i>=100:
        
            print(i,company,"update")
            stock_update(company)
            sleep(1)
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

class StockDescList(generics.ListAPIView):
    # queryset = Stockdesc.objects.all()
    serializer_class = StockDescSerialzier
    lookup_field = 'symbol'
    def get_queryset(self):
        print(self.kwargs)
        # original qs
        qs = super().get_queryset() 
        # filter by a variable captured from url, for example
        return qs.filter(name__startswith=self.kwargs['name'])

class StockDescDetail(generics.RetrieveAPIView):
    queryset = Stockdesc.objects.all()
    serializer_class = StockDescSerialzier
    lookup_field = 'symbol'


class StockEntire(generics.RetrieveAPIView):
    queryset = UsStocklist.objects.all()
    serializer_class = StockPageEntireSerializer
    lookup_field = 'symbol'


import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep





def crawl_news(ticker,driver):
    driver.get('https://www.stockwatch.com/Quote/Detail?U:'+ticker)
    try:
        table = driver.find_element_by_id("MainContent_NewsList1_Table1_Table1")
        tbody = table.find_element_by_tag_name("tbody")
        rows = tbody.find_elements_by_tag_name("tr")
        href_url = []
        alist = table.find_elements_by_tag_name('a')
        for i,ahref in enumerate(alist):
            if i%2==0:
                continue
            news_url = ahref.get_attribute('href')
            href_url.append(news_url)
        sleep(1)
        df = []
        for index, value in enumerate(rows):
            body = value.find_elements_by_tag_name("td")
            line = []
            for j , content in enumerate(body):
                line.append(content.text)
            line.append(href_url[index])
            df.append(line)
        df_tbl = pd.DataFrame(df,columns=('date','symbol','release','title','url'))   #index 지정
        df_tbl.drop("symbol",axis=1,inplace=True) # 불필요한 column 제거
        df_tbl.drop("release",axis=1,inplace=True) # 불필요한 column 제거
        print(df_tbl)
        return df_tbl
    except:
        return pd.DataFrame()

def get_contents_news(news_url,driver):
    news_list = []
    for url in news_url:
        driver.get(url)
        contents = driver.find_element_by_id('MainContent_NewsText').text
        contents = re.sub('\n','',contents) # 개행 제거
        contents = re.sub('\t','',contents)
        contents = re.sub('   ',' ',contents)
        if len(contents)>5000:
            contents = contents[:5000]
        news_list.append(contents)
    return news_list




# 리눅스 환경에서만 작동
# def news_translate(news):
#     tl = Pororo(task="translation", lang="multi")
#     summ_tool = Pororo(task="summarization", model="abstractive", lang="ko")
#     tl = tl(news,src='en',tgt='ko')
#     summ = summ_tool(tl, model="abstractive", lang="ko")
#     return summ



def get_dataframe(ticker):
    driver = webdriver.Chrome('C:/Users/Jinho/DjangoProjects/hojae/stock/chromedriver.exe')

    news_df = crawl_news(ticker,driver) #
    if news_df.empty:
        print("no")
        return pd.DataFrame()
    news_df = news_df.loc[:4,]
    news_url = news_df["url"] # 뉴스 링크
    news_list = get_contents_news(news_url,driver)
    news_df["contents"] = news_list # 영어 본문 column 추가
    return news_df
    # else:
    #     return None

import yahoo_fin.stock_info as si

class abc(APIView):
    def get(self,request):
        objects = UsStocklist.objects.all()

        for i,object in enumerate(objects):
            if StockAdditional.objects.filter(symbol = object).exists():
                continue
            print(object)
            symbol = object.symbol
            print(i,symbol)
            query_symbol = symbol.replace('.','-') # 티커명 yahoofinance에 맞게 변경
            df = si.get_quote_table(query_symbol)


            market_cap = df['Market Cap']
            eps = df['EPS (TTM)']
            per = df['PE Ratio (TTM)']
            if StockAdditional.objects.filter(symbol = object).exists():
                print('yes')
                data = StockAdditional.objects.filter(symbol = object)
                data.market_cap = market_cap
                data.eps = eps
                data.per = per
                data.save()
            StockAdditional.objects.create(
                symbol = object,
                market_cap = market_cap,
                eps = eps,
                per = per
            )
            sleep(2)








@api_view(['GET'])
def entire_stock_news(request):
    objects = UsStocklist.objects.all()

    
    for i,object in enumerate(objects):
        if i>=147:
            ticker = object.symbol
            print(i,ticker)
            symbol = UsStocklist.objects.get(symbol = ticker)
            news_df = get_dataframe(ticker)
            if news_df.empty:
                continue
            for i,news in enumerate(news_df.itertuples()):
                _,date,title,url,content = news
                date = date.split(' ')[0]
                if Newscontents.objects.filter(title = title).exists():
                    print(ticker,"news exists, terminate")
                    break
                Newscontents.objects.create(symbol = symbol,date = date,title=title,url = url, content = content )
                print(ticker,"news create")

            sleep(1)
    return Response({"message":"entire description success"},status = 200)


def entire_news_tranlate(request):
    """
    뉴스제목 번역 api
    """
    objects = Newscontents.objects.all()
    for i,object in enumerate(objects):
        print(object.title)
        if object.title_translation:
            continue
        url = 'https://openapi.naver.com/v1/papago/n2mt'

        CLIENT_ID = 'SNh7rE2sRKalR1ZtUXvY'
        CLIENT_SECRET = 'ITlIneA0zE'
        # CLIENT_ID = 'i_8pC2lDwjUX3tizVzyP'
        # CLIENT_SECRET = 'tVQDEBkV0f'

        headers = {
            "Content-Type" : "application/json",
            "X-Naver-Client-Id" : CLIENT_ID,
            "X-Naver-Client-Secret":CLIENT_SECRET
        }
        params = {
            "source" : "en",
            "target" : "ko",
            "text" : object.title
        }
        response = requests.post(url,json.dumps(params),headers = headers)
        msg = response.json()["message"]["result"]["translatedText"]
        object.title_translation = msg
        object.save()
        sleep(1)

class NewsContentsList(APIView):
    def get(self,request,symbol,*args,**kwargs):
        stock = UsStocklist.objects.filter(symbol=symbol).exists # 해당 blog 댓글
        if stock:
            symbol = UsStocklist.objects.get(symbol = symbol)
            queryset = Newscontents.objects.filter(symbol = symbol)
            print(queryset)
            if queryset:
                serializer = NewsContentsSerializer(queryset,many =True)
                return Response(serializer.data)
            return Response({"message": "news does not exist"})
            
        else:
            return Response({"message":"stock does not exist"})
class CustomResultsSetPagination(PageNumberPagination):
     page_size = 10 
     page_size_query_param = 'page_size'


class NewsEntireList(generics.ListAPIView):
    queryset = Newscontents.objects.all()
    serializer_class = NewsContentsSerializer
    # pagination_class = CustomResultsSetPagination

class NewsLatest(generics.ListAPIView):
    queryset = Newscontents.objects.all()[:10]
    serializer_class =NewsContentsSerializer