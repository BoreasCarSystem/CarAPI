from django.conf.urls import url
from django.contrib import admin
from userpage import views


urlpatterns = [

    url(r'^status/$', views.status),

]

