from django.urls import path
from ..views import BlogList

"""
CLIENT
Base ENDPOINT   /boards/

"""

urlpatterns = [
    path('<str:symbol>/',BlogList.as_view()),
    # path('<str:symbol>/create/',blog_create_view),
    # path('<str:symbol>/<int:pk>/',blog_detail_view),
    # path('<str:symbol>/<int:pk>/update/',blog_detail_view),
    # path('<str:symbol>/<int:pk>/delete/',blog_detail_view),
]