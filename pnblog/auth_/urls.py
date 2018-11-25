from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('hello' , views.hello , name = "hello"),
    path('login/', views.login, name='login'),
    path('logout/', views.Logout.as_view()),
    path('register/' , views.register , name = 'register')
]