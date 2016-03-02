from django.db import models
import json

# Create your models here.


class Message(models.Model):
    def convert_boolean(self, str):
        if str == "true":
            return True
        elif str == "false":
            return False
        else:
            raise ValueError("Unrecognized boolean value " + str)

    def convert_float(self, str):
        return float(str)

    def __str__(self):
        return "Set " + self.type + " to " + self.value


    MESSAGE_CONVERTERS = {
        "AC_enabled": convert_boolean,
        "AC_temperature": convert_float
    }

    MESSAGE_TYPE = (
                ('AC_enabled', "Set air condition status"),
                ('AC_temperature', "Set air condition temperature")

    )

    type = models.CharField(max_length=30, choices=MESSAGE_TYPE, primary_key=True)
    value = models.CharField(max_length=50)

    def get_json_object(self):
        return {"type": self.type, "value": self.MESSAGE_CONVERTERS[self.type](self, self.value)}



