from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from . import views
# app_name = "yougam"

urlpatterns = [
    path('', views.post, name = "index"),
    path('<int:video>/detail/', views.detail, name='detail'),
    path('<str:video>/change/<int:cid>/<str:senti>', views.change, name='change'),
    path('<int:video>/creator/', views.creator, name='creator'),
    path('user/',views.user, name='user'),
    path('youtube/<int:video>/first_show/', views.first_show, name='first_show'),
    path('youtube/', views.post6, name='post6'),
    path('youtube/<int:video>/show/', views.show, name='shows'),
    path('youtube_type/', views.typeRecieve, name='typeRecieve'),
]
