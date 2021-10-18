
from stock import serializers
from ..serializers import UsStockDailySerializer, UsStockListSerailzer,IncomeStatementSerializer
from ..models import UsStocklist,UsCompanyDaily,IncomeStatement
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

@api_view(['GET'])
def incomeStatement_view(request,symbol,*args,**kwargs):
    """
    기업 손익계산서
    revenue : 매출
    gross_profit : 매출총이익 = 매출 - 매출원가
    operating_income : 영업이익 = 매출총이익 - (판매비+관리비)
    net_income : 당기순이익 = 세후 순이익
    """
    company = IncomeStatement.objects.filter(company_code=symbol)
    serializer = IncomeStatementSerializer(company,many = True)
    return Response(serializer.data)
    