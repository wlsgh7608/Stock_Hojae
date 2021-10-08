from rest_framework import serializers
from stock.models import UsCompanyDaily, UsStocklist
class UsStockListSerailzer(serializers.ModelSerializer):
    class Meta:
        model = UsStocklist
        fields = ['symbol','name','industry','industry_id']

class UsStockDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsCompanyDaily
        fields = ['stock_date','company_code','close','open','high','low','volume','change']