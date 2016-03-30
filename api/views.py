from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Message
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


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
    json_string = request.body.decode("utf-8")
    # Parse JSON
    data_from_pi = json.loads(json_string)
    # Print the received data
    if settings.DEBUG:
        print(data_from_pi)
    # TODO: Save these data so they can be accessed by the user later
    return create_response()


@csrf_exempt
def error(request):
    return create_response()