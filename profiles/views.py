from django.http.response import JsonResponse
from django.shortcuts import render
import jwt

# Create your views here.
from rest_framework import permissions
from rest_framework.fields import ReadOnlyField
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from hojae.settings import SECRET_KEY
from core.utils import LoginConfirm 
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
User = get_user_model()
class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class Check(APIView):
    """
    JWT 전송하면 해당 유저 반환 
    """
    @LoginConfirm
    def get(self,request):
        username = request.user.username
        query = User.objects.get(username=username) 
        serializer = UserSerializer(query, many=False) 
        context = {'message':"success",'data':serializer.data}
        return Response(context)
        
class UserList(APIView):
    """
    유저이름 중복확인
    """
    permission_classes = [AllowAny] 
    # User list를 보여줄 때
    def get(self,request,*args,**kwargs):
        check_username = request.data['username']
        Users = User.objects.filter(username = check_username)
        if Users:
            return Response({"message":"already exists"},status=400)
        else:
            return Response({"message":"available username"},status = 200)