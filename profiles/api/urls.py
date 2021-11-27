from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token,verify_jwt_token

from ..views import CreateUserView,Check, TodoDetail,UserList,TodoListView,BookMarkList,BookMarkDetail,KakaoLoginView

"""
CLIENT
Base ENDPOINT   /users/

"""
urlpatterns = [
    path('register/', CreateUserView.as_view()), # 회원가입
    path('check/',Check.as_view()), # jwt 토큰으로 유저 확인
    path('login/',obtain_jwt_token), #jwt 토큰 획득

    path('refresh/',refresh_jwt_token), # jwt 토큰 갱신
    path('verify/',verify_jwt_token), # jwt 토큰 확인
    path('usercheck/',UserList.as_view()), 
    path('todolist/',TodoListView.as_view()), # 유저별 todolist
    path('todo/<int:todo_id>/',TodoDetail.as_view()), # todolist 상세

    path('bookmark/',BookMarkList.as_view()),
    path('bookmark/<int:bookmark_id>/',BookMarkDetail.as_view()),


    path('kakao/login/',KakaoLoginView.as_view()),
] 
