
from stock import serializers
from ..serializers import UsStockDailySerializer, UsStockListSerailzer
from ..models import UsStocklist,UsCompanyDaily
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def us_stocklist_view(request,*args,**kwargs):
    """
    미국주식 리스트 출력
    """
    stocklist = UsStocklist.objects.all()
    serializer = UsStockListSerailzer(stocklist,many = True)
    return Response(serializer.data)

@api_view(['GET'])
def us_stockdaily_view(request,symbol,*args,**kwargs):
    """
    주식 일일데이터 출력
    """
    stock = UsCompanyDaily.objects.filter(company_code=symbol)
    serializer = UsStockDailySerializer(stock,many = True)
    return Response(serializer.data)