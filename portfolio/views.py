from django.core import paginator
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.views import APIView

from core.utils import LoginConfirm
from stock.models import CurrentStock, UsStocklist
from stock.views import stock_update
from .models import GamePortfolio, PortfolioName,Portfolio,InvestGame
from rest_framework import generics, serializers
from .serializers import GameRankSerializer, InvestGameSerializer, PortfolioNameSerializer,PortfolioEntireSerializer, PortfolioSerializer
from rest_framework.response import Response
# Create your views here.
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone


class PortfolioList(generics.ListCreateAPIView):
    queryset = PortfolioName.objects.all()
    serializer_class = PortfolioEntireSerializer



class apicheck(APIView):
    def get(self,*args,**kargs):
        pnames = PortfolioName.objects.all()
        serializer = PortfolioNameSerializer(pnames,many= True)
        return Response(serializer.data)
    
class checkehcek(generics.ListCreateAPIView):
    queryset = PortfolioName.objects.all()
    serializer_class = PortfolioEntireSerializer

class PortfolioNameListView(APIView):
    """
    GET/POST
    """
    def get(self,request,*args,**kwargs):
        user_portfolios = PortfolioName.objects.filter(user = request.user)
        if not user_portfolios:
            return Response({"message":"does not exist"},status=404)
        serializer = PortfolioNameSerializer(user_portfolios,many = True)
        return Response(serializer.data)

    @LoginConfirm
    def post(self,request,*args,**kwargs):
        if len(PortfolioName.objects.filter(user = request.user))>=5:
            return Response({"message":"포트폴리오는 최대 5개까지 가능합니다."})
        serializer = PortfolioNameSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data,status = 201)
        return Response(serializer.errors,status = 400)

class PortfolioNameDetailView(APIView):
    """
    GET/Update/Delete
    """
    def get(self,request,portfolio_name_id,*args,**kwargs):
        portfolio = PortfolioName.objects.get(pk = portfolio_name_id) or None
        if portfolio:   
            serializer = PortfolioNameSerializer(portfolio)
            return Response(serializer.data)
        return Response({"message":"portfolio does not exist"},status = 404)

    @LoginConfirm
    def put(self,request,portfolio_name_id,*args,**kwargs):
        portfolio = PortfolioName.objects.get(pk = portfolio_name_id) or None
        if portfolio:
            if portfolio.user != request.user:
                return Response({"message":"different user!"},status = 400)
            serializer = PortfolioNameSerializer(data = request.data, instance=portfolio)
            if serializer.is_valid():
                serializer.save(user = request.user)
                return Response(serializer.data,status = 201)
            return Response(serializer.errors,status = 400)
        return Response({"message":"portfolio does not exist"},status = 404)
    

    
    @LoginConfirm
    def delete(self,request,portfolio_name_id,*args,**kwargs):
        portfolio = PortfolioName.objects.get(pk = portfolio_name_id)
        if portfolio:
            if portfolio.user!= request.user:
                return Response({"message":"different user!"},status=  400)
            portfolio.delete()
            return Response({"message":"portfolio deleted"})
        return Response({"message":"portfolio does not exist"},status = 404)

class PortfolioListView(APIView):
    """
    GET/POST
    """
    def get(self,request,portfolio_name_id,*args,**kwargs):
        portfolios = Portfolio.objects.filter(portfolio = portfolio_name_id)
        if portfolios:
            serializer = PortfolioSerializer(portfolios,many = True)
            return Response(serializer.data)
        else:
            return Response({"message":"portfolioName does not exist"},status = 404)

    @LoginConfirm
    def post(self,request,portfolio_name_id,*args,**kwargs):
        print(request)
        print(request.body)
        print(request.data)
        if len(Portfolio.objects.filter(portfolio = portfolio_name_id))>=30:
            return Response({"message":"포트폴리오당 종목은 최대 30개까지 가능합니다."})
        portfolioName = PortfolioName.objects.get(pk = portfolio_name_id)
        serializer = PortfolioSerializer(data = request.data)
        if serializer.is_valid() :
            if request.user == portfolioName.user:
                serializer.save(portfolio= portfolioName)
                return Response(serializer.data,status = 201)
            else:
                return Response({"message":"different user! please check user"})
        return Response(serializer.errors,status = 400)


class PortfolioDetailView(APIView):
    """
    GET/Update/Delete
    """
    def get(self,request,portfolio_id,*args,**kwargs):
        portfolio = Portfolio.objects.get(pk = portfolio_id) or None
        if portfolio:   
            serializer = PortfolioSerializer(portfolio)
            return Response(serializer.data)
        return Response({"message":"portfolio does not exist"},status = 404)

    @LoginConfirm
    def put(self,request,portfolio_id,*args,**kwargs):
        portfolio = Portfolio.objects.get(pk = portfolio_id) or None
        if portfolio:
            if portfolio.portfolio.user != request.user:
                return Response({"message":"different user!"},status = 400)
            serializer = PortfolioSerializer(data = request.data, instance=portfolio)
            if serializer.is_valid():
                serializer.save(user = request.user)
                return Response(serializer.data,status = 201)
            return Response(serializer.errors,status = 400)
        return Response({"message":"portfolio does not exist"},status = 404)
    
    @LoginConfirm
    def delete(self,request,portfolio_id,*args,**kwargs):
        portfolio = Portfolio.objects.get(pk = portfolio_id)
        if portfolio:
            if portfolio.portfolio.user!= request.user:
                return Response({"message":"different user!"},status=  400)
            portfolio.delete()
            return Response({"message":"portfolio deleted"})
        return Response({"message":"portfolio does not exist"},status = 404)
    

class PortfolioShare(APIView):
    @LoginConfirm
    def get(self,request,portfolio_name_id, *args,**kwargs):
        portfolioname = PortfolioName.objects.filter(pk= portfolio_name_id).exists()
        if portfolioname:
            object = PortfolioName.objects.get(pk = portfolio_name_id)
            if object.user != request.user:
                return Response({"message": "diffrent user"})
            else:
                if object.isshare == True:
                    object.isshare = False
                elif object.isshare == False:
                    object.isshare = True
                    object.share_date = timezone.now()
                object.save()
                return Response({"message": "share function success"})
        else:
            return Response({"message":"portfolio does not exist"})


class PortfolioShareList(APIView):
    
    def get(self,request,*args,**kwargs):
        objects = PortfolioName.objects.filter(isshare = True)
        if objects:
            serializer = PortfolioNameSerializer(objects, many = True)
            return Response(serializer.data)
        else:
            return Response({"message" : "portfoliolist does not exist"})


class InvestGameView(APIView):
    @LoginConfirm
    def get(self,request,*args,**kwargs):
        invest = InvestGame.objects.filter(user = request.user)
        if invest:
            serializer = InvestGameSerializer(invest,many=True)
            return Response(serializer.data)
        return Response({"message":"investgame does not exist"})

    @LoginConfirm
    def post(self,request):
        user = request.user
        if InvestGame.objects.filter(user=request.user).exists():
            return Response({"message":"investgame alreaey exists"})
        InvestGame.objects.create(user = user)
        data = InvestGame.objects.get(user=user)
        serializer = InvestGameSerializer(data)
        return Response(serializer.data)

class GameStockView(APIView):

    @LoginConfirm
    def post(self,request,account_id,*args,**kwargs):
        game_account = InvestGame.objects.get(pk = account_id)
        if game_account.user != request.user:
            return Response({"message":"different user!"})

        data = request.data
        action = data['action']
        if int(data['number'])<=0:
            return Response({"message":"number can't be negative"})

        stock_list = game_account.stocks.all()
        isexist = False
        symbol = UsStocklist.objects.get(symbol = data['symbol'])
        symbol_data = None
        for i,stock in enumerate(stock_list):
                if stock.symbol == symbol: # 현재 모의투자에 해당 symbol 존재 
                    isexist = True
                    symbol_data= stock
                    break
                
        if action == 'buy':
            # serializer = PortfolioSerializer(data = request.data)
            stock_price = CurrentStock.objects.get(symbol = symbol)
            if game_account.cash <stock_price.close*int(data['number']):
                return Response({"message": "can't buy! you need enough cash!"})
            game_account.cash -= stock_price.close*int(data['number'])
            game_account.save()
            if symbol_data:
                new_number = symbol_data.number + int(data['number'])
                previous_sum = symbol_data.value*symbol_data.number
                new_sum = stock_price.close*int(data['number'])
                symbol_data.value = (previous_sum + new_sum)/new_number
                symbol_data.number += int(data['number'])
                symbol_data.save()
            else:
                
                GamePortfolio.objects.create(
                    game_account = game_account,
                    symbol = symbol,
                    number = int(data['number']),
                    value = stock_price.close,
                )
            return Response({"message":"buy success"})
        elif action == 'sell':
            if isexist:
                if int(data['number'])>symbol_data.number: #파려는 수량이 가지고 있는 것보다 많을 경우
                    return Response({"message": "sell number is more than existing stock number"})
                stock_price = CurrentStock.objects.get(symbol = symbol)
                game_account.cash += int(data['number'])*stock_price.close
                game_account.save()
                symbol_data.number -= int(data['number'])
                if symbol_data.number:
                    symbol_data.save()
                else:
                    symbol_data.delete()
                return Response({"message":"sell success"})
            
            else:
                return Response({"message":"symbol does not exist"})



class InvestGameRank(APIView):
    def get(self,request):
        objects = InvestGame.objects.all()
        if objects:
            serializer = GameRankSerializer(objects,many=True)
            sort_serializer = sorted(serializer.data,key = lambda x: x['estimated'],reverse=True)
            return Response(sort_serializer)
        return Response({"message":"investgame does not exist"})