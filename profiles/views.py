from django.http.response import JsonResponse
from django.shortcuts import render
import jwt
import requests
# Create your views here.
from rest_framework import permissions
from rest_framework import generics
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.generics import CreateAPIView
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from hojae.settings import SECRET_KEY
from core.utils import LoginConfirm
from .serializers import UserSerializer,TodolistSerializer,BookMarkSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from .models import TodoList,BookMark
# from .models import UserTodoList
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

class TodoListView(APIView):
    permission_classes = [IsAuthenticated]

    @LoginConfirm
    def get(self,request,*args,**kwargs):
        user_todo = TodoList.objects.filter(user = request.user)
        if not user_todo:
            return Response({"message":"todo does not exist"})
        serializer = TodolistSerializer(user_todo,many = True)
        return Response(serializer.data)

    @LoginConfirm
    def post(self,request,*args,**kwargs):
        serializer = TodolistSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data,status = 201)
        return Response(serializer.errors,status = 400)

class TodoDetail(APIView):
    """
    GET/Update/Delete
    """

    def get(self,request,todo_id,*args,**kwargs):
        todo = TodoList.objects.get(pk = todo_id) or None
        if todo:   
            if todo.user != request.user:
                return Response({"message":"different user!"},status = 400)
            
            serializer = TodolistSerializer(todo)
            return Response(serializer.data)
        return Response({"message":"todo does not exist"},status = 404)

    @LoginConfirm
    def put(self,request,todo_id,*args,**kwargs):
        todo = TodoList.objects.get(pk = todo_id) or None
        if todo:
            if todo.user != request.user:
                return Response({"message":"different user!"},status = 400)
            serializer = TodolistSerializer(data = request.data, instance=todo)
            if serializer.is_valid():
                serializer.save(user = request.user)
                return Response(serializer.data,status = 201)
            return Response(serializer.errors,status = 400)
        return Response({"message":"todo does not exist"},status = 404)
    
    @LoginConfirm
    def delete(self,request,todo_id,*args,**kwargs):
        todo = TodoList.objects.get(pk = todo_id)
        if todo:
            if todo.user!= request.user:
                return Response({"message":"different user!"},status=  400)
            todo.delete()
            return Response({"message":"todo deleted"})
        return Response({"message":"todo does not exist"},status = 404)


class BookMarkList(APIView):
    permission_classes = [IsAuthenticated]

    @LoginConfirm
    def get(self,request,*args,**kwargs):
        queryset = BookMark.objects.filter(user = request.user)
        if not queryset:
            return Response({"message":"bookmark does not exist"})
        serializer = BookMarkSerializer(queryset,many= True)
        return Response(serializer.data)

    @LoginConfirm
    def post(self,request,*args,**kwargs):
        symbol = request.headers.get("symbol",None)
        serializer = BookMarkSerializer(request.data)
        if serializer.is_valid():
            serializer.save(user = request.user,bookmark_symbol = symbol)
            return Response(serializer.data,status = 201)
        else:
            return Response(serializer.errors)


class BookMarkDetail(APIView):
    permission_classes = [IsAuthenticated]

    @LoginConfirm
    def get(self,request,symbol,*args,**kwargs):
        queryset = BookMark.objects.filter(user = request.user).filter(bookmark_symbol = symbol)
        serializer = BookMarkSerializer(queryset,many= True)
        return Response(serializer.data)

    @LoginConfirm
    def delete(self,request,bookmark_id,*args,**kwargs):
        bookmark = BookMark.objects.get(pk = bookmark_id)
        if bookmark:
            if bookmark.user!= request.user:
                return Response({"message":"different user!"},status=  400)
            bookmark.delete()
            return Response({"message":"bookmark deleted"})
        return Response({"message":"bookmark does not exist"},status = 404)


import json
from django.views import View
from django.http import JsonResponse,HttpResponse
from django.conf import settings

class KakaoLoginView(View):
    def get(self,request):
        code = request.GET.get('code',None)

        url = 'https://kauth.kakao.com/oauth/token'
        headers = {'Content-type':'application/x-www-form-urlencoded; charset=utf-8'}

        body = {'grant_type' : 'authorization_code',
        'client_id':'68e30f3899d1d63604741dd7d8123880',
        'redirect_uri':'http://127.0.0.1:8000/users/kakao/login/',
        'code':code}

        token_kakao_response = requests.post(url,headers=headers,data=body)
        # return HttpResponse(f'{token_kakao_response.text}')


        access_token = json.loads(token_kakao_response.text).get('access_token')
        url = "https://kapi.kakao.com/v2/user/me" # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 카카오 API 주소
        headers      ={
            'Authorization' : f"Bearer {access_token}"}

        kakao_response = requests.get(url,headers=headers)
        kakao_response = json.loads(kakao_response.text)
        email = kakao_response['kakao_account']['email']
        nickname = kakao_response['properties']['nickname']
        isexist = User.objects.filter(email =email ).exists()
        print("if ",isexist)
        if isexist:
            # 존재
            # user = 
            pass
        else:
            # 존재 X
            new_user = User(
                username = nickname,
                email = email
            )
            new_user.save()

        return HttpResponse(f'good')




    


# class KakaoLoginView(APIView):

    # def get(self, request,*args,**kwargs):
    #     print("check")
    #     print(args,kwargs)
    #     print(request.data)
    #     access_token = request.headers["Authorization"]
    #     headers      =({'Authorization' : f"Bearer {access_token}"})
    #     url          = "https://kapi.kakao.com/v1/user/me" # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 카카오 API 주소
    #     response     = requests.request("POST", url, headers=headers) # API를 요청하여 회원의 정보를 response에 저장
    #     user         = response.json()
    #     print(user)

    #     if User.objects.filter(social_login_id = user['id']).exists(): #기존에 소셜로그인을 했었는지 확인
    #         user_info          = User.objects.get(social_login_id=user['id'])
    #         encoded_jwt        = jwt.encode({'id': user_info.id}, settings.SECRET_KEY, algorithm='HS256') # jwt토큰 발행

    #         return JsonResponse({ #jwt토큰, 이름, 타입 프론트엔드에 전달
    #             'access_token' : encoded_jwt.decode('UTF-8'),
    #             'user_name'    : user_info.name,
    #             'user_pk'      : user_info.id
    #         }, status = 200)            
    #     else:
    #         new_user_info = User(
    #             social_login_id = user['id'],
    #             name            = user['properties']['nickname'],
    #             social          = SocialPlatform.objects.get(platform ="kakao"),
    #             email           = user['properties'].get('email', None)
    #         )
    #         new_user_info.save()
    #         encoded_jwt         = jwt.encode({'id': new_user_info.id}, wef_key, algorithm='HS256') # jwt토큰 발행
    #         none_member_type    = 1
    #         return JsonResponse({
    #             'access_token' : encoded_jwt.decode('UTF-8'),
    #             'user_name'    : new_user_info.name,
    #             'user_pk'      : new_user_info.id,
    #             }, status = 200)