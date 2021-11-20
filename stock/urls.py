from django.urls import path
from .views import currentStocklist,individual_stock_update,entire_stock_update,entire_stock_desc,StockDescList,StockDescDetail,StockEntire,entire_stock_news,entire_news_tranlate
app_name = 'stock'
"""
/stock/
"""

urlpatterns = [
    path('api/current/',currentStocklist.as_view()),
    path('',entire_stock_update),
    path('list/<str:symbol>/',individual_stock_update),
    path('description/',StockDescList.as_view()),
    path('description/<str:symbol>/',StockDescDetail.as_view()),
    path('description/entire/<str:symbol>/',StockEntire.as_view()),
    
    # path('entire/news/',entire_stock_news)
    path('entire/translate/',entire_news_tranlate)
    
]