from rest_framework.response import Response
from django.shortcuts import render
from django.http.response import HttpResponse
import FinanceDataReader as fdr

from stock.serializers import CurrentStockSerializer
from .models import CurrentStock, UsCompanyDaily,UsStocklist
import pandas as pd
import datetime
from rest_framework.decorators import api_view
from time import sleep
from rest_framework.generics import ListAPIView
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
    # tsla_date = UsCompanyDaily.objects.filter(company_code__in = company).first().stock_date
    # next_date = tsla_date+datetime.timedelta(days=1)
    # print(symbol,next_date)
    # symbol_data = fdr.DataReader(symbol,next_date) # 2010년부터 일일데이터 로드
    # for j,row in enumerate(symbol_data.itertuples()):
    #     print(row)
    #     s_date,close,open,  high , low, volume,change  = row # unpacking
    #     s_date = s_date.strftime("%y-%m-%d")
    #     volume = int(volume)
    #     change = round(change,5)
    #     column = "company_code_id,stock_date,close,open,high,low,volume,change"
    #     data = symbol,s_date,close,open,high,low,volume,change
    #     print(data) 
        # data = c_name,s_date,close,open,high,low,volume,change

        # db.insertDB(schema='public',table='stock_uscompanydaily',column=column,data=data)

    # company_list = fdr.StockListing("NYSE")[:50]
    # company_list = pd.concat(company_list, ignore_index=True)
    # print(company_list)
    # context = {'company_list':company_list}
    # return render(request,'stock/company_list.html',context)
    return Response({'message':'good'})




# def stockUpdate(request,)