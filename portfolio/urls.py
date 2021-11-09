from django.urls import path
from .views import PortfolioList,apicheck
"""
CLIENT
Base ENDPOINT   /portfolio/

"""

urlpatterns = [
    path('',PortfolioList.as_view()),
    path('check/',apicheck.as_view()),
    # path(),

]