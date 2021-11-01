from .models import Blog

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
class PublicProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields =[
            'username',
            'id',
        ] 


class BlogSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    class Meta:
        model = Blog
        fields = ['user','symbol','id','title','create_date','body','modify_date']

    def validate_content(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("내용이 너무 깁니다.(500자)")
        return value




   