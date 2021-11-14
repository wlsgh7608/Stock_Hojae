from django.urls import path
from .views import currentStocklist,individual_stock_update,entire_stock_update,entire_stock_desc
app_name = 'stock'


urlpatterns = [
    path('api/current/',currentStocklist.as_view()),
    path('',entire_stock_update),
    path('list/<str:symbol>/',individual_stock_update),
    # path('api/desc/',entire_stock_desc)
    
]