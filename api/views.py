from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Message, FloatData, BooleanData, StringData
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


import json
# Create your views here.

def create_response():
    messages = Message.objects.all()

    json_objects = [msg.get_json_object() for msg in messages]

    if settings.DELETE_FETCHED_MESSAGES:
        messages.delete()

    if len(json_objects) == 0:
        return HttpResponse()

    # set safe to false to allow list as root
    return JsonResponse(json_objects, safe=False)


"""Make an exception from CSRF, since the PI will make POST
requests and the authenticity of the requests will be ensured other ways"""
@csrf_exempt
def status(request):


    # Decode the POST body, so it can be read by json.load

    if (request.method == "POST"):
        json_string = request.body.decode("utf-8")

        # Parse JSON
        data_from_pi = json.loads(json_string)

        for key in data_from_pi:
            value = data_from_pi[key]
            print(key)

            if isinstance(value, float):
                try:
                    data = FloatData.objects.get(pk=key)
                    data.value = value
                    data.save()
                except ObjectDoesNotExist:
                    FloatData.objects.create(key=key, value=value)
            elif isinstance(value, bool):
                try:
                    data = BooleanData.objects.get(pk=key)
                    data.value = value
                    data.save()
                except ObjectDoesNotExist:
                    BooleanData.objects.create(key=key, value=value)
            elif isinstance(value, str):
                try:
                    data = StringData.objects.get(pk=key)
                    data.value = value
                    data.save()
                except ObjectDoesNotExist:
                    StringData.objects.create(key=key, value=value)


        # Print the received data
        if settings.DEBUG:
            pass
        print(data_from_pi)
    # TODO: Save these data so they can be accessed by the user later
    return create_response()


@csrf_exempt
def error(request):
    return create_response()