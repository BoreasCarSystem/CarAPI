from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Message
from django.conf import settings

import json
# Create your views here.

def create_response():
    messages = Message.objects.all()

    json_objects = [msg.get_json_object() for msg in messages]

    if settings.DELETE_FETCHED_MESSAGES:
        messages.delete()

    # set safe to false to allow list as root
    return JsonResponse(json_objects, safe=False)


def status(request):
    return create_response()


def error(request):
    return create_response()