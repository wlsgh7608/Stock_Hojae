from django.urls import path
from .views import PortfolioNameListView,PortfolioNameDetailView,PortfolioListView,PortfolioDetailView
"""
CLIENT
Base ENDPOINT   /portfolio/

"""

urlpatterns = [
    path('user/',PortfolioNameListView.as_view()),
    path('user/detail/<int:portfolio_name_id>/',PortfolioNameDetailView.as_view()),
    path('user/list/<int:portfolio_name_id>/',PortfolioListView.as_view()), # portfolio 해당하는 종목 출력

    path('<int:portfolio_id>/',PortfolioDetailView.as_view()),



    # path(),

]