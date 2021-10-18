# from profiles.api.views import tweet_feed_view
from django.urls import path
from .views import (
    us_stocklist_view,
    us_stockdaily_view,
    incomeStatement_view,
    balanceSheet_view,
    
)

"""
CLIENT
Base ENDPOINT   /api/stock/

"""

urlpatterns = [
 
    path('',us_stocklist_view),
    path('<str:symbol>/',us_stockdaily_view),
    path('<str:symbol>/incomestatement/',incomeStatement_view),
    path('<str:symbol>/balancesheet/',balanceSheet_view),
   

 
] 
