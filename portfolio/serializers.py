from django.db import models
from django.db.models.query_utils import select_related_descend
from rest_framework import serializers

from stock.views import stock_update
from .models import GamePortfolio, InvestGame, PortfolioName,Portfolio
from stock.models import CurrentStock



class PortfolioNameSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model =  PortfolioName
        # fields = ('username','name')
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    profitloss = serializers.SerializerMethodField()
    profitloss_margin = serializers.SerializerMethodField()

    def get_profitloss(self,obj):
        if CurrentStock.objects.filter(symbol = obj.symbol).exists(): # currentstock에 존재 할시
            stock_price = CurrentStock.objects.get(symbol = obj.symbol).close # 객체 가져옴
            return round((stock_price-obj.value)*obj.number,3)
        else:
            return 0.0 # current에 존재하지 않을 때 손실0
    def get_profitloss_margin(self,obj):
        return round(self.get_profitloss(obj)/(obj.number*obj.value)*100,2) # 수익률 체크

    class Meta:
        model  = Portfolio
        fields = ('id','user','symbol','number','value','profitloss','profitloss_margin')
        # fields = '__all__'

class PortfolioEntireSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source = 'user.username')
    portfolio_set = PortfolioSerializer(many=True, read_only=True)
    class Meta:
        model = PortfolioName
        fields = ('id','username','portfolio_set','name')





class GamePortfolioSerializer(serializers.ModelSerializer):
    profitloss = serializers.SerializerMethodField()
    profitloss_margin = serializers.SerializerMethodField()

    def get_profitloss(self,obj):
        stock_price = CurrentStock.objects.get(symbol = obj.symbol).close # 객체 가져옴
        return round((stock_price-obj.value)*obj.number,3)

    def get_profitloss_margin(self,obj):
        return round(self.get_profitloss(obj)/(obj.number*obj.value)*100,2) # 수익률 체크
    
    class Meta:
        model = GamePortfolio
        fields = ('id','symbol','number','value','profitloss','profitloss_margin')


class InvestGameSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source  = 'user.username')
    estimated = serializers.SerializerMethodField()
    stocks = GamePortfolioSerializer(many = True,read_only = True)

    def get_estimated(self,obj):
        # 추정 금액
        game_stocks = obj.stocks.all()
        total = obj.cash
        for stock in game_stocks:
            total += stock.number * CurrentStock.objects.get(symbol = stock.symbol).close 
        return total
    
    class Meta:
        model = InvestGame
        fields = ('id','username','cash','estimated','stocks')