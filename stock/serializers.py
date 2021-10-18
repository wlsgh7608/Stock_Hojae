from rest_framework import serializers
from stock.models import IncomeStatement, UsCompanyDaily, UsStocklist
class UsStockListSerailzer(serializers.ModelSerializer):
    class Meta:
        model = UsStocklist
        fields = ['symbol','name','industry','industry_id']

class UsStockDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsCompanyDaily
        fields = ['stock_date','company_code','close','open','high','low','volume','change']


class IncomeStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model : IncomeStatement
        fields = ['company_code','end_date','revenue','gross_profit','operating_income','net_income']