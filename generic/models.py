from django.db import models
from django.forms import DateTimeField
from django.db.models import Model, CharField, DateTimeField, TextField, URLField

#Table for Alarm
class Alarm(Model):
    header = CharField(max_length=100, unique=True)
    content = TextField()
    date = DateTimeField()
    url = URLField(max_length=1000, blank=True, null=True)
    icon_tag = CharField(max_length=50, default="fa-bell", blank=True, null=True)

#Table for Message
class Notifications(Model):
    header = CharField(max_length=100, unique=True)
    content = TextField()
    date = DateTimeField()
    url = URLField(max_length=1000, blank=True, null=True)
    icon_tag = CharField(max_length=50, default="fa-envelope", blank=True, null=True)
