from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader

from api.models import FloatData, BooleanData, StringData, Message, ErrorMessage
from django.core.exceptions import ObjectDoesNotExist
import time as tm

# Create your views here.


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
        {"name": "A/C status", "value": ac_enabled, "image": "userpage/icons/Fan-96.png"}
    ]
    context = {"sensors": sensor_values, "warning": find_errors()}
    return render(request=request, template_name="userpage/status.html", context=context)


def temperature(request):
    context = dict()
    if request.method == "POST":
        try:
            activate_temperature(request)
        except ValueError as e:
            context["warning"] = e.args[0]

    context["AC_temperature"] = getDataValue("temperature", FloatData.objects, "°C")
    context["AC_enabled"] = getDataValue("AC_enabled", BooleanData.objects, replace_true_with="On", replace_false_with="Off")
    if "warning" not in context:
        context["warning"] = find_errors()

    return render(request=request, template_name="userpage/temperature.html", context=context)


def activate_temperature(request) :
    post = dict(request.POST)

    if "temperature" in post:
        try:
            temp = float((post["temperature"][0]).strip())
            create_temperature_message(temp)
        except:
            raise ValueError("Temperature must be a number", "temperature")

    if "time" not in post:
        if "hours" in post and "minutes" in post:
            try:
                time = post["hours"][0] + ":" + post["minutes"][0]
                tm.strptime(time, "%H:%M")	#Raiser valueError om regexen ikke matcher
                create_time_message(time)
            except ValueError:
                raise ValueError("Time must be in the format \"HH:MM\"", "time")
        
    if "AC_enabled" in post:
        enabled = post["AC_enabled"][0]
        if enabled == "True":
            create_AC_enabled_message(enabled)
        else:
            raise ValueError("AC_enabled is not boolean", "AC_enabled")


def deactivate_temperature(request):
    post = dict(request.POST)

    if "AC_enabled" in post:
        enabled = post["AC_enabled"][0]
        if enabled == "False":
            create_AC_enabled_message(enabled)
        else:
            raise ValueError("AC_enabled is not boolean", "AC_enabled")


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


def create_AC_enabled_message(enabled):
    message = Message()
    message.type = "AC_enabled"
    message.value = enabled
    message.save()


def find_errors():
    errors = ErrorMessage.objects.all()
    warning_message = "<br/>".join((str(error) for error in errors))
    ErrorMessage.objects.all().delete()
    return warning_message
