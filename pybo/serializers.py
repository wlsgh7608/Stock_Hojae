from .models import Blog,Comment

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings

from profiles.serializers import UserSerializer


User = get_user_model()
class PublicProfileSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField(read_only = True)

     class Meta:
        model = User
        # fields = ( "id", "username" )
        fields = '__all__'




class BlogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Blog
        fields = '__all__'

    def validate_content(self, body):
        
        if len(body) > 500:
            raise serializers.ValidationError("내용이 너무 깁니다.(500자)")
        return body


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def validate_content(self, content):
        if len(content) > 500:
            raise serializers.ValidationError("내용이 너무 깁니다.(500자)")
        return content

   