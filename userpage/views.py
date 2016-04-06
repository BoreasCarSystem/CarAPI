from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from api.models import FloatData, BooleanData, StringData
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


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
    context = {"sensors": sensor_values}
    return render(request=request, template_name="userpage/status.html", context=context)


def temperature(request):
    return render(request=request, template_name="userpage/temperature.html")