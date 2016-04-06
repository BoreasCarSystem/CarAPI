from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from api.models import Message


# Create your views here.
thing = "<html><head><title>yes</title></head><body>YOU DID IT</body></html>"

def status(request):
    sensor_values = [
        {"name": "Current temperature:", "value": "21 °C", "image": "userpage/icons/Temperature-96.png"},
        {"name": "Battery Level:", "value": "full"},
    ]
    context = {"sensors": sensor_values}
    return render(request=request, template_name="userpage/status.html", context=context)


def temperature(request):
    return render(request=request, template_name="userpage/temperature.html")


def activate_temperature(request):
    if request.method == "POST":
        temp = url_parser(request)

        temp_message = Message()
        temp_message.type = "AC_temperature"
        temp_message.value = temp
        temp_message.save()

        return HttpResponse(status=200, content="hei")


def url_parser(request):
    data = dict(request.POST)
    temp = None

    if "temperature" in data:
        temp = data["temperature"][0]

    return temp
