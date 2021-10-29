from django.http.response import HttpResponse
from django.shortcuts import render,get_object_or_404

from pybo.serializers import BlogSerializer
from .models import Blog,Comment
from rest_framework import serializers, viewsets
# Create your views here.
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from core.utils import LoginConfirm
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from stock.models import UsStocklist

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
                print("serializer adsfasfasdf asd : ",serializer.data)
                return Response(serializer.data, status=201)
            else:
                return Response({"messsage":"symbol does not exist"},status=400)

        return Response(serializer.errors, status=400)



@api_view(['GET'])
def blog_list_view(request,symbol,*args,**kwargs):
    serializer = BlogSerializer



@api_view(['GET'])
def blog_detail_view(request,symbol,pk,*args,**kwargs):
    print(symbol,pk)
    print(args,kwargs)
    
    serializer = BlogSerializer



def index(request):
    """
    pybo 목록 출력
    """
    question_list = Blog.objects.order_by('-create_date')
    context = {'question_list':question_list}
    return render(request,'pybo/question_list.html',context)
def detail(request,question_id):
    """
    pybo 목록 출력
    """
    question = get_object_or_404(Blog,pk = question_id)
    context = {'question':question}
    return render(request,'pybo/question_detail.html',context)