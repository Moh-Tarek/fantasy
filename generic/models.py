from django.db import models
from django.forms import DateTimeField
from django.db.models import Model, CharField, DateTimeField, TextField

#Table for Alarm
class Alarm(Model):
    alarm_header = CharField(max_length=100, unique=True)
    alarm_content = TextField()
    alarm_date = DateTimeField()

#Table for Message
class Notifications(Model):
    notifications_header = CharField(max_length=100, unique=True)
    notifications_content = TextField()
    notifications_date = DateTimeField()
