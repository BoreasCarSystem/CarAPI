from django.conf.urls import url
from django.contrib import admin
from userpage import views


urlpatterns = [

    url(r'^status/$', views.status, name="status"),
    url(r'^temperature/$', views.temperature, name="temperature"),
    url(r'^temperature/data/$', views.temperature_data, name="temperaturedata")
]

