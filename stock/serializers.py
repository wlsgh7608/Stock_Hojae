from django.db import models
from django.db.models import fields
from rest_framework import serializers
from stock.models import IncomeStatement, StockAdditional, Stockdesc, UsCompanyDaily, UsStocklist,BalanceSheet,CurrentStock,Newscontents
class UsStockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsStocklist
        fields = ['symbol','name','industry','industry_id']

class UsStockDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsCompanyDaily
        fields = ['stock_date','company_code','close','open','high','low','volume','change']
class IncomeStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeStatement
        # fields = "__all__"
        fields = ['company_code','end_date','revenue','gross_profit','operating_income','net_income']



class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheet
        fields = ['company_code','end_date','total_liability','total_stockholder_equity','total_assets','total_current_assets','total_current_liability']

class CurrentStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentStock
        fields = ['symbol','close','open','high','low','volume','change','date']

class StockDescSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Stockdesc
        fields = '__all__'
class StockAdditoinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAdditional
        fields = '__all__'


class StockPageEntireSerializer(serializers.ModelSerializer):
    incomestatement_set = IncomeStatementSerializer(read_only = True,many=True)
    balancesheet_set = BalanceSheetSerializer(read_only= True,many= True)
    stockadditional_set = StockAdditoinalSerializer(read_only = True,many = True)
    stockdesc = StockDescSerialzier(read_only = True)
    # income = IncomeStatementSerializer(read_only = True,many= True)
    # test = serializers.IntegerField(default = 0)

    class Meta:
        model = UsStocklist
        # fields = ['symbol','name','balance','income']
        fields = '__all__'

class NewsContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newscontents
        fields = ('id','date','url','title','translation','symbol','title_translation')