from django.urls import path
from ..views import BlogList,BlogDetailView,UserList,BlogEntireList

"""
CLIENT
Base ENDPOINT   /boards/

"""

urlpatterns = [
    path('',BlogEntireList.as_view()),
    path('<str:symbol>/',BlogList.as_view()),
    path('<str:symbol>/<int:blog_id>/',BlogDetailView.as_view()),
]