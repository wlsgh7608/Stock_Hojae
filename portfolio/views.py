from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.views import APIView
from .models import PortfolioName
from rest_framework import generics, serializers
from .serializers import PortfolioNameSerializer,PortfolioEntireSerializer
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