from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from rest_framework.decorators import api_view , permission_classes
from .models import Post, Comment , Repost
from .serializers import UserSerializer , PostSerializer, CommentSerializer , RepostSerializer
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
import json
from django.core import serializers

def hello(request):
    str = 'hello'
    return HttpResponse(str)

class PostPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.is_authenticated:
                return True
            return False
        elif request.method == 'GET':
            return True
        else:
            return True

    def has_object_permission(self, request, view, obj):
        print(1)
        if request.method == 'DELETE' or request.method == 'PUT':
            print(request.user)
            print(obj.author)
            return request.user == obj.author
        else:
            return True

class CommentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        else:
            return True
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' or request.method == 'PUT':
            return request.user == obj.author
        else:
            return True


class RepostPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        else:
            return True
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' or request.method == 'PUT':
            return request.user == obj.author
        else:
            return True

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermissions, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermissions,)

    def get(self, request, pk , *args, **kwargs):
        post = Post.objects.get(id = pk)
        serializer = PostSerializer(post , many = False)
        comments = Comment.objects.filter(post = post).values('text' , 'author' , 'create_date')
        newdict = json.dumps(list(comments))
        newdict.update(serializer.data)
        return Response(newdict, status=status.HTTP_201_CREATED)

@api_view(['GET' , 'POST'])
@permission_classes((CommentPermissions, ))
def comment_list(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments , many = True)
        return Response(serializer.data)
    else:
        serializer = CommentSerializer(data = request.data)
        post_id = request.data.get('post_id')
        post = Post.objects.get(id = post_id)
        if serializer.is_valid():
            serializer.save(author = request.user , post = post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE' , 'GET' , 'PUT'])
@permission_classes((CommentPermissions, ))
def comment_detail(request , pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((CommentPermissions, ))
def add_comment(request , pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET' , 'POST'])
@permission_classes((RepostPermissions, ))
def repost_list(request):
    if request.method == 'GET':
        reposts = Repost.objects.all()
        serializer = RepostSerializer(reposts , many = True)
        return Response(serializer.data)


@api_view(['DELETE' , 'GET' , 'PUT'])
@permission_classes((RepostPermissions, ))
def repost_detail(request , pk):
    try:
        repost = Repost.objects.get(id=pk)
    except Repost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = RepostSerializer(repost)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        repost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((RepostPermissions, ))
def do_repost(request , pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RepostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
