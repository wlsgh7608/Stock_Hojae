from django.urls import path
from .views import individual_stock_update,entire_stock_update
app_name = 'stock'


urlpatterns = [
    path('',entire_stock_update),
    path('list/<str:symbol>/',individual_stock_update)
]