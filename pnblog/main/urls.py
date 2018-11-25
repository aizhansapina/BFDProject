from . import views
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('hello', views.hello),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('comments/', views.comment_list),
    path('comments/<int:pk>/', views.comment_detail),
    path('posts/<int:pk>/comments/' , views.add_comment),
    path('reposts/', views.repost_list),
    path('reposts/<int:pk>/', views.repost_detail),
    path('posts/<int:pk>/reposts/' , views.do_repost),
]

urlpatterns = format_suffix_patterns(urlpatterns)