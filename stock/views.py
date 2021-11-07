from rest_framework.response import Response
from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render,get_object_or_404
import FinanceDataReader as fdr
from .models import UsCompanyDaily,UsStocklist
import pandas as pd
import datetime

# Create your views here.


def daily_update(symbol,date):
    company = UsStocklist.objects.filter(symbol = symbol)
    current_date = UsCompanyDaily.objects.filter(company_code_in = company).first().stock_date
    next_date = current_date+datetime.timedelta(days= 1)

    stock_data = fdr.DataReader(symbol,next_date) # 다음날부터 update
    for j,row in enumerate(stock_data.itertuples()):
        print(row)
        s_date,close,open,  high , low, volume,change  = row # unpacking
        s_date = s_date.strftime("%y-%m-%d")
        volume = int(volume)
        change = round(change,5)
        column = "company_code_id,stock_date,close,open,high,low,volume,change"
        data = symbol,s_date,close,open,high,low,volume,change
        print(data) 






def index(request):
    symbol = 'TSLA'
    company = UsStocklist.objects.filter(symbol = symbol)
    tsla_date = UsCompanyDaily.objects.filter(company_code__in = company).first().stock_date
    next_date = tsla_date+datetime.timedelta(days=1)
    print(symbol,next_date)
    symbol_data = fdr.DataReader(symbol,next_date) # 2010년부터 일일데이터 로드
    for j,row in enumerate(symbol_data.itertuples()):
        print(row)
        s_date,close,open,  high , low, volume,change  = row # unpacking
        s_date = s_date.strftime("%y-%m-%d")
        volume = int(volume)
        change = round(change,5)
        column = "company_code_id,stock_date,close,open,high,low,volume,change"
        data = symbol,s_date,close,open,high,low,volume,change
        print(data) 
        # data = c_name,s_date,close,open,high,low,volume,change

        # db.insertDB(schema='public',table='stock_uscompanydaily',column=column,data=data)

    # company_list = fdr.StockListing("NYSE")[:50]
    # company_list = pd.concat(company_list, ignore_index=True)
    # print(company_list)
    # context = {'company_list':company_list}
    # return render(request,'stock/company_list.html',context)
    return Response({'message':'good'})




# def stockUpdate(request,)