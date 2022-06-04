from django.contrib import admin
from .models import Alarm, Notifications

admin.site.register(Alarm)
admin.site.register(Notifications)