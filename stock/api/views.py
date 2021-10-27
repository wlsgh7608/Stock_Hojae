
from stock import serializers
from ..serializers import BalanceSheetSerializer, UsStockDailySerializer, UsStockListSerializer,IncomeStatementSerializer
from ..models import BalanceSheet, UsStocklist,UsCompanyDaily,IncomeStatement
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import AllowAny,IsAuthenticated



# @api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JSONWebTokenAuthentication,))
class StocklistView(ListAPIView):
    """
    미국주식 리스트 출력
    """
    permission_classes = [AllowAny,]
    authentication_classes = [JSONWebTokenAuthentication,]
    queryset = UsStocklist.objects.all()
    serializer_class = UsStockListSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('symbol','name')


# @api_view(['GET'])
# @permission_classes((AllowAny, ))
# @authentication_classes((JSONWebTokenAuthentication,))
# def us_stocklist_view(request,*args,**kwargs):
#     stocklist = UsStocklist.objects.all()
#     serializer = UsStockListSerializer(stocklist,many = True)
#     return Response(serializer.data)
    

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JSONWebTokenAuthentication,))
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
    기업 손익계산서( 단위 : $1,000)
    revenue : 매출
    gross_profit : 매출총이익 = 매출 - 매출원가
    operating_income : 영업이익 = 매출총이익 - (판매비+관리비)
    net_income : 당기순이익 = 세후 순이익
    """
    company = IncomeStatement.objects.filter(company_code=symbol)
    serializer = IncomeStatementSerializer(company,many = True)
    return Response(serializer.data)


@api_view(['GET'])
def balanceSheet_view(request,symbol,*args,**kwargs):
    """
    기업 재무상태표( 단위 : $1,000)
    total_liability : 총부채비용
    total_stockholder_equity : 자기자본
    total_assets : 총 자산
    total_current_assets  유동 자산 = 1년 안에 현금화가능한 자산
    total_current_liability 유동 부채 = 1년 안에 갚아야하는 자산
    """
    company = BalanceSheet.objects.filter(company_code=symbol)
    serializer = BalanceSheetSerializer(company,many = True)
    return Response(serializer.data)