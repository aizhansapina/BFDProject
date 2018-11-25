from rest_framework import serializers
from .models import Post, Comment , Repost
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=300)
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    class Meta:
        model = Post
        fields = ['id' , 'title' , 'content' , 'category' , 'author' , 'create_date']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    post = PostSerializer(read_only = True)

    class Meta:
        model = Comment
        fields = ['id' , 'text', 'post' , 'author' , 'create_date']

class RepostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    post = PostSerializer(read_only = True)

    class Meta:
        model = Repost
        fields = ['post' , 'user' , 'create_date']