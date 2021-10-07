
from stock import serializers
from ..serializers import UsStockListSerailzer
from ..models import UsStocklist
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def us_stocklist_view(request,*args,**kwargs):
    stocklist = UsStocklist.objects.all()
    serializer = UsStockListSerailzer(stocklist,many = True)
    return Response(serializer.data)
