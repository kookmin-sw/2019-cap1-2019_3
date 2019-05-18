from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
# app_name = "yougam"

urlpatterns = [
    path('', views.post, name = "index"),
    path('<str:video>/change/<int:cid>/<str:senti>', views.change, name='change'),
    path('user/',views.user, name='user'),
    path('<int:video>/user/', views.userdetail, name='userdetail'),
    path('youtube_type/<int:video>/creator/', views.crtdetail, name='crtdetail'),
    url(r'^sending/$', views.sending, name='sending'),    #webcam json message
]

# 서버에서 이미지 받아올때, 경로 추가
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # add