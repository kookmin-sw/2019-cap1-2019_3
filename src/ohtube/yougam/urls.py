from django.conf.urls import url
from django.contrib import admin
from . import views
app_name = "yougam"

urlpatterns = [
    url(r'^$', views.post, name = "index"),
    url(r'^(?P<video>[0-9]+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<video>[0-9]+)/change/(?P<cid>[0-9]+)/(?P<senti>[0-9]+)$', views.change, name='change'),
    url(r'^(?P<video>[0-9]+)/creator$', views.creator, name='creator'),
    url(r'^user',views.user, name='user')
]
