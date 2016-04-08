from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader

from api.models import FloatData, BooleanData, StringData, Message
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

thing = "<html><head><title>yes</title></head><body>YOU DID IT</body></html>"

def getDataValue(pk, objects, suffix=""):
    try:
        value = objects.get(pk=pk).value
        if isinstance(value, float):
            value = round(value, 1)
        return str(value) + " " + suffix
    except ObjectDoesNotExist:
        return "N/A"



def status(request):


    battery_level = getDataValue("battery_level", FloatData.objects, "%")
    fuel_level = getDataValue("fuel_level", FloatData.objects, "%")
    temperature = getDataValue("temperature", FloatData.objects, "°C")
    washerfluid_level = getDataValue("washerfluid_level", FloatData.objects, "%")
    ac_status = getDataValue("ac_status", StringData.objects)


    sensor_values = [
        {"name": "Current temperature:", "value": temperature, "image": "userpage/icons/Temperature-96.png"},
        {"name": "Battery Level:", "value": battery_level, "image":"userpage/icons/Charged Battery-96.png"},
        {"name": "Fuel Level", "value": fuel_level,"image":"userpage/icons/Gas Station-96.png"},
        {"name": "Washerfluid Level", "value": washerfluid_level, "image":"userpage/icons/Water-96.png"},
        {"name": "Oil Level", "value": "OK", "image": "userpage/icons/Oil Industry-96.png"},
        {"name": "A/C status", "value": ac_status, "image":"userpage/icons/Fan-96.png"}
    ]
    context = {"sensors": sensor_values, "warning": "Insert warning here, or remove it to have no warning."}
    return render(request=request, template_name="userpage/status.html", context=context)


def temperature(request):
    if request.method == "POST":
        activate_temperature(request)

    return render(request=request, template_name="userpage/temperature.html")


def activate_temperature(request):
    post = dict(request.POST)

    if "temperature" in post:
        create_temperature_message(post["temperature"][0])

    if "time" in post:
        create_time_message(post["time"][0])


def create_temperature_message(temperature):
    message = Message()
    message.type = "AC_temperature"
    message.value = temperature
    message.save()

def create_time_message(time):
    message = Message()
    message.type = "AC_timer"
    message.value = time
    message.save()
