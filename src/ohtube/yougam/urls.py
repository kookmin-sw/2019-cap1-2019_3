from django.conf.urls import url
from django.contrib import admin
from . import views
app_name = "yougam"

urlpatterns = [
    url(r'^$', views.post, name = "first"),
    url(r'^(?P<video>[0-9]+)/detail/$', views.detail, name='detail'),

]
