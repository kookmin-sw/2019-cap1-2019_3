from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from . import views
# app_name = "yougam"

urlpatterns = [
    path('', views.post, name = "index"),
    path('<str:video>/change/<int:cid>/<str:senti>', views.change, name='change'),
    path('user/',views.user, name='user'),
    path('<int:video>/user/', views.userdetail, name='userdetail'),
    path('youtube_type/<int:video>/creator/', views.crtdetail, name='crtdetail'),
]
