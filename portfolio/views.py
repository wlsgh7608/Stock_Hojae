from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.views import APIView

from core.utils import LoginConfirm
from .models import PortfolioName,Portfolio
from rest_framework import generics
from .serializers import PortfolioNameSerializer,PortfolioEntireSerializer, PortfolioSerializer
from rest_framework.response import Response
# Create your views here.



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