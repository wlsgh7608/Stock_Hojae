from django.urls import path
from ..views import BlogList,BlogDetailView,BlogEntireList,CommentListView,CommentDetailView

"""
CLIENT
Base ENDPOINT   /boards/

"""

urlpatterns = [
    path('blog/',BlogEntireList.as_view()),
    path('blog/<str:symbol>/',BlogList.as_view()),
    path('blog/<str:symbol>/<int:blog_id>/',BlogDetailView.as_view()),

    path('comments/<int:blog_id>/',CommentListView.as_view()), # 블로그의 댓글 리스트
    path('comment/<int:comment_id>/',CommentDetailView.as_view()) # comment_id
]