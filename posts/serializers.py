from rest_framework import serializers

from users.serializers import ProfileSerializer
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ['author']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'text']


class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)   # nested serializer
    comments = CommentSerializer(many=True, read_only=True)   # many=True : 다수의 댓글 포함

    class Meta:
        model = Post
        exclude = ['author']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'category', 'body', 'image']
