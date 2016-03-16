from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.


def status(request):
    return HttpResponse("OK")

def temperature(request):

    return render(request=request, template_name="userpage/temperature.html")