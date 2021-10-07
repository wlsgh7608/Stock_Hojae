from rest_framework import serializers
from stock.models import UsStocklist
class UsStockListSerailzer(serializers.ModelSerializer):
    class Meta:
        model = UsStocklist
        fields = ['symbol','name','industry','industry_id']
