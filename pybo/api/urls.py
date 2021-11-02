from django.urls import path
from ..views import BlogList,BlogDetailView,UserList

"""
CLIENT
Base ENDPOINT   /boards/

"""

urlpatterns = [
    path('<str:symbol>/',BlogList.as_view()),
    path('<str:symbol>/<int:blog_id>/',BlogDetailView.as_view()),
    path('<str:symbol>/usertest/',UserList.as_view()),
    # path('<str:symbol>/<int:pk>/delete/',blog_detail_view),
]