from rest_framework import serializers
from .models import PortfolioName,Portfolio




class PortfolioNameSerializer(serializers.Serializer):
    class Meta:
        model =  PortfolioName
        fields = '__all__'


class PortfolioSerializer(serializers.Serializer):
    profitloss = serializers.SerializerMethodField()
    profitloss_margin = serializers.SerializerMethodField()



    class Meta:
        model  = Portfolio
        fields = '__all__'