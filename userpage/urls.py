from django.conf.urls import url
from django.contrib import admin
from userpage import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name="temperature")),
    url(r'^status/$', views.status, name="status"),
    url(r'^temperature/$', views.temperature, name="temperature"),
    url(r'^temperature/data/$', views.temperature_data, name="temperaturedata")
]

