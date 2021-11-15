from django.urls import path
from .views import currentStocklist,individual_stock_update,entire_stock_update,entire_stock_desc,StockDescList,StockDescDetail
app_name = 'stock'


urlpatterns = [
    path('api/current/',currentStocklist.as_view()),
    path('',entire_stock_update),
    path('list/<str:symbol>/',individual_stock_update),
    path('desc/',StockDescList.as_view()),
    path('desc/<str:symbol>/',StockDescDetail.as_view())
    # path('api/desc/',entire_stock_desc)
    
]