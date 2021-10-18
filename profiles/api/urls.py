from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token,verify_jwt_token



"""
CLIENT
Base ENDPOINT   /api-jwt-auth/

"""

urlpatterns = [
    path('',obtain_jwt_token), #jwt 토큰 획득
    path('refresh/',refresh_jwt_token), # jwt 토큰 갱신
    path('verify/',verify_jwt_token), # jwt 토큰 확인
   

 
] 
