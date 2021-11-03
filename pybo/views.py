from django.contrib.auth import get_user_model
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render,get_object_or_404
from rest_framework import permissions
from rest_framework.fields import ReadOnlyField

from pybo.serializers import BlogSerializer, CommentSerializer,PublicProfileSerializer
from profiles.serializers import UserSerializer
from .models import Blog,Comment
from rest_framework import serializers, viewsets
# Create your views here.
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from core.utils import LoginConfirm
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from stock.models import UsStocklist

from django.utils import timezone

User = get_user_model()
class UserList(APIView):
    permission_classes = [AllowAny]
    
    # User list를 보여줄 때
    def get(self,*args,**kwargs):
        Users = User.objects.all()
        print(Users)
        serializer = UserSerializer(Users, many=True)
        return Response(serializer.data)


class BlogEntireList(APIView):
    permissions_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request,*args,**kwargs):
        blogs = Blog.objects.all()
        blogs = blogs.order_by('-create_date')
        serializer = BlogSerializer(blogs,many = True)

        return Response(serializer.data)

        
class BlogList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly] # 인증받은사람이 아니면 읽기만 가능

    # Blog list를 보여줄 때
    def get(self,request,symbol,*args,**kwargs):
        blogs = Blog.objects.filter(symbol=symbol)
        blogs = blogs.order_by('-create_date') # 시간역순으로 정렬
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    

    # 새로운 Blog 글을 작성할 때
    @LoginConfirm
    def post(self,request,symbol):
        # request.data는 사용자의 입력 데이터
        symbol = UsStocklist.objects.get(symbol = symbol) or None
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            if symbol: # symbol 객체가 존재할 시 
                serializer.save(user = request.user,symbol = symbol) # 저장
                return Response(serializer.data, status=201)
            else:
                return Response({"messsage":"symbol does not exist"},status=400)
        return Response(serializer.errors, status=400)



class BlogDetailView(APIView):
    permissions = [IsAuthenticatedOrReadOnly] # 인증된 사람만


    def get(self,request,symbol,blog_id,*args,**kwargs):
        blogs = Blog.objects.filter(symbol=symbol)
        blog = blogs.get(pk = blog_id)
        print(blog)
        blog.hits +=1
        blog.save()
        serializers = BlogSerializer(blog)
        return Response(serializers.data)

    #Update
    @LoginConfirm
    def put(self,request,symbol,blog_id,*args,**kwargs):
        blogs = Blog.objects.filter(symbol=symbol)
        blog = blogs.get(pk = blog_id)
        serializer = BlogSerializer(data = request.data , instance = blog)
        if blog.user != request.user:
            return Response({"message": "사용자가 다릅니다. "},status = 400)
        if serializer.is_valid(): #유효성 검사
            print(timezone.now())
            serializer.save(modify_date = timezone.now()) # 저장
            return Response(serializer.data, status=201) # Update 성공
        else:
            return Response({"messsage":"symbol does not exist"},status=400)
    #Delete
    @LoginConfirm
    def delete(self,request,blog_id,*args,**kwargs):
        blog = Blog.objects.get(pk=blog_id) or None
        if blog:
            if blog.user != request.user:
                print("different user!")
                return Response({"message":"different user!"},status= 400)
            else:
                blog.delete()
                return Response({"message":"blog delete success"})
        else:
            return Response({"message":"blog does not exist"},status = 404)
class CommentListView(APIView):
    # Read
    def get(self,request,blog_id,*args,**kwargs):
        blog = Blog.objects.get(pk= blog_id)
        comments = Comment.objects.filter(question=blog) # 해당 blog 댓글
        comments = comments.order_by('-create_date')
        if comments:
            serializers = CommentSerializer(comments,many = True)
            return Response(serializers.data)
        else:
            return Response({"message":"blog does not exist"},status = 404)

    # Create
    @LoginConfirm
    def post(self,request,blog_id,*args,**kwargs):
        # request.data는 사용자의 입력 데이터
        blog = Blog.objects.get(pk = blog_id)
        if blog:
            serializer = CommentSerializer(data = request.data)
            if serializer.is_valid(): #유효성 검사
                serializer.save(user = request.user,question = blog) # 저장
                return Response(serializer.data, status=201)
        else:
            return Response({"message":"blog does not exist"},status = 404)
        return Response(serializer.errors, status=400)

class CommentDetailView(APIView):
    permissions = [IsAuthenticatedOrReadOnly]
    # Read
    def get(self,request,comment_id,*args,**kwargs):
        comments = Comment.objects.get(pk=comment_id)
        if comments:
            serializers = CommentSerializer(comments)
            return Response(serializers.data)
        else:
            return Response({"message":"blog does not exist"},status = 404)

    # Update
    @LoginConfirm
    def put(self,request,comment_id,*args,**kwargs):
        comment = Comment.objects.get(pk=comment_id) or None
        print(comment)
        serializer = CommentSerializer(data = request.data,instance=comment)
        if comment:
            if comment.user != request.user:
                return Response({"message":"different user!"},status= 400)
            if serializer.is_valid(): #유효성 검사
                serializer.save(modify_date = timezone.now()) # 저장
                return Response(serializer.data, status=201) # Update 성공
        else:
            return Response({"message":"comment does not exist"},status = 404)


    # Delete
    @LoginConfirm
    def delete(self,request,comment_id,*args,**kwargs):
        comment = Comment.objects.get(pk=comment_id) or None
        serializer = CommentSerializer(data = request.data,instance=comment)
        if comment:
            if comment.user != request.user:
                return Response({"message":"different user!"},status= 400)
            else:
                comment.delete()
                return Response({"message":"comment delete success"})
        else:
            return Response({"message":"comment does not exist"},status = 404)


    