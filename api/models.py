from django.db import models
import json
import datetime
import time
from django.core.exceptions import ValidationError

# Create your models here.



class Message(models.Model):
    def convert_boolean(self, str):
        str = str.lower()
        if str == "true":
            return True
        elif str == "false":
            return False
        else:
            raise ValueError("Unrecognized boolean value " + str)

    def convert_float(self, str):
        return float(str)

    def convert_time(self, str):
        return str

    def __str__(self):
        return "Set " + self.type + " to " + self.value


    MESSAGE_CONVERTERS = {
        "AC_enabled": convert_boolean,
        "AC_temperature": convert_float,
        "AC_timer": convert_time
    }

    MESSAGE_TYPE = (
                ('AC_enabled', "Set air condition status"),
                ('AC_temperature', "Set air condition temperature"),
                ('AC_timer', "Set activation time for the AC")

    )

    type = models.CharField(max_length=30, choices=MESSAGE_TYPE, primary_key=True)
    value = models.CharField(max_length=50)

    def get_json_object(self):
        return {"type": self.type, "value": self.MESSAGE_CONVERTERS[self.type](self, self.value)}



class FloatData(models.Model):

    key = models.CharField(max_length=50, primary_key=True)
    value = models.FloatField(editable=True)

    def __str__(self):
        return self.key + ": " + str(self.value)

class BooleanData(models.Model):

    key = models.CharField(max_length=50, primary_key=True)
    value = models.BooleanField(editable=True)

     def __str__(self):
        return self.key + ": " + str(self.value)

class StringData(models.Model):

    key = models.CharField(max_length=50, primary_key=True)
    value = models.CharField(max_length=200, editable=True)

     def __str__(self):
        return self.key + ": " + str(self.value)