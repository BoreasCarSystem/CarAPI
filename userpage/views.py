from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.


def status(request):
    sensor_values = [
        {"name": "Current temperature:", "value": "21 °C", "image": "userpage/icons/Temperature-96.png"},
        {"name": "Battery Level:", "value": "full"},
    ]
    context = {"sensors": sensor_values, "warning": "Insert warning here, or remove it to have no warning."}
    return render(request=request, template_name="userpage/status.html", context=context)


def temperature(request):
    return render(request=request, template_name="userpage/temperature.html")