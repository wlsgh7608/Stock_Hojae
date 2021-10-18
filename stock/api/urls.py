# from profiles.api.views import tweet_feed_view
from django.urls import path
from .views import (
    us_stockdaily_view,
    incomeStatement_view,
    balanceSheet_view,
    StocklistView,
    
)

"""
CLIENT
Base ENDPOINT   /api/stock/

"""

urlpatterns = [
 
    path('',StocklistView.as_view()),
    # path('search/',StocklistView.as_view()),
    path('<str:symbol>/',us_stockdaily_view),
    path('<str:symbol>/incomestatement/',incomeStatement_view),
    path('<str:symbol>/balancesheet/',balanceSheet_view),
   

 
] 
