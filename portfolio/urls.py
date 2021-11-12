from django.urls import path
from .views import PortfolioNameListView,PortfolioNameDetailView,PortfolioListView,PortfolioDetailView
"""
CLIENT
Base ENDPOINT   /portfolio/



/portfolio/user/ # 포트폴리오 이름 리스트
/protfolio/user/포트폴리오이름 번호 # 포트폴리오 각각 

/portfolio/list/포트폴리오이름번호 # 포트폴리오에 해다하는 종목들 출력
/portfolio/포트폴리오번호 # 포트폴리오의 한 종목 

"""

urlpatterns = [
    path('user/',PortfolioNameListView.as_view()),
    path('user/<int:portfolio_name_id>/',PortfolioNameDetailView.as_view()),
    
    path('list/<int:portfolio_name_id>/',PortfolioListView.as_view()), # portfolio 해당하는 종목 출력
    path('<int:portfolio_id>/',PortfolioDetailView.as_view()),

]