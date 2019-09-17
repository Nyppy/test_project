from .models import Post
from django.utils import timezone
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_date = serializers.HiddenField(default=timezone.now())
    published_date = serializers.HiddenField(default=timezone.now())

    class Meta:
        model = Post
        fields = '__all__'
