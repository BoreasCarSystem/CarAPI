from django.contrib import admin
from .models import Message, FloatData, BooleanData, StringData, ErrorMessage
# Register your models here.

admin.site.register(Message)
admin.site.register(FloatData)
admin.site.register(BooleanData)
admin.site.register(StringData)
admin.site.register(ErrorMessage)