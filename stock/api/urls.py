# from profiles.api.views import tweet_feed_view
from django.urls import path
from .views import (
    us_stocklist_view,
    us_stockdaily_view,
    
)

"""
CLIENT
Base ENDPOINT   /api/stock/

"""

urlpatterns = [
 
    path('',us_stocklist_view),
    path('<str:symbol>/',us_stockdaily_view),
   

 
] 
