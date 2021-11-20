from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model

from profiles.models import BookMark, TodoList
# from .models import User

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only = True)

    def validate(self, attrs):
        #password1과 password2가 맞지않으면
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 맞지 않습니다.","password2":"비밀번호가 맞지 않습니다."})
        return attrs
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password","password2" )

class TodolistSerializer(serializers.ModelSerializer):

    def validate_todolist(self,todolist):
        if len(todolist)>50:
            raise serializers.ValidationError({"todolist":"todolist가 너무 깁니다."})
        return todolist

    class Meta:
        model = TodoList
        fields = ('id','todolist')


class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = '__all__'

# class UserCreateSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)

#     def create(self, validated_data):
#         user = User.objects.create(
#             email=validated_data['email'],
#             username=validated_data['username'],
#         )
#         user.set_password(validated_data['password'])

#         user.save()
#         return user