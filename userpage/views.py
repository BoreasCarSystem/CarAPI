from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader

from api.models import FloatData, BooleanData, StringData, Message
from django.core.exceptions import ObjectDoesNotExist
import time

# Create your views here.

thing = "<html><head><title>yes</title></head><body>YOU DID IT</body></html>"


def getDataValue(pk, objects, suffix=None, replace_true_with=None, replace_false_with=None):
    try:
        value = objects.get(pk=pk).value
        value_string = None

        if isinstance(value, float):
            value = round(value, 1)
            value_string = str(value)
        elif isinstance(value, bool):
            if value and replace_true_with:
                value_string = replace_true_with
            elif not value and replace_false_with:
                value_string = replace_false_with
        if not value_string:
            value_string = str(value)
        if suffix:
            return value_string + " " + suffix
        return value_string
    except ObjectDoesNotExist:
        return "N/A"


def status(request):

    battery_level = getDataValue("battery_level", FloatData.objects, "%")
    fuel_level = getDataValue("fuel_level", FloatData.objects, "%")
    temperature = getDataValue("temperature", FloatData.objects, "°C")
    washerfluid_level = getDataValue("washerfluid_level", FloatData.objects, "%")
    ac_enabled = getDataValue("AC_enabled", BooleanData.objects, replace_true_with="On", replace_false_with="Off")

    sensor_values = [
        {"name": "Current temperature:", "value": temperature, "image": "userpage/icons/Temperature-96.png"},
        {"name": "Battery Level:", "value": battery_level, "image":"userpage/icons/Charged Battery-96.png"},
        {"name": "Fuel Level", "value": fuel_level,"image":"userpage/icons/Gas Station-96.png"},
        {"name": "Washerfluid Level", "value": washerfluid_level, "image":"userpage/icons/Water-96.png"},
        {"name": "Oil Level", "value": "OK", "image": "userpage/icons/Oil Industry-96.png"},
        {"name": "A/C status", "value": ac_enabled, "image":"userpage/icons/Fan-96.png"}
    ]
    context = {"sensors": sensor_values, "warning": "Insert warning here, or remove it to have no warning."}
    return render(request=request, template_name="userpage/status.html", context=context)


def temperature(request):
    context = dict()
    if request.method == "POST":
        try:
            activate_temperature(request)
        except ValueError as e:
            context["warning"] = e.args[0]

    return render(request=request, template_name="userpage/temperature.html", context=context)


def activate_temperature(request) :
    post = dict(request.POST)

    if "temperature" in post:
        try:
            temp = float(post["temperature"][0].strip())
            create_temperature_message(temp)
        except:
            raise ValueError("Temperature must be a number", "temperature")

    if "time" in post:
        try:
            time = post["time"][0]
            time.strptime(time, "%H:%M")
            create_time_message(time)

        except ValueError:
            raise ValueError("Time must be in the format \"HH:MM\"", "time")


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
