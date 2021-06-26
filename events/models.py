from django.db import models
from validators import *


class Event(models.Model):

    your_name = models.CharField(max_length=54, blank=False, null=False, 
        validators=[alpha])
    your_email = models.EmailField(max_length=254, null=False, blank=False)
    your_number = models.CharField(max_length=20, null=False, blank=False, 
        validators=[phone])
    your_message = models.TextField(max_length=540, null=False, blank=False)
    event_type = models.ForeignKey('EventType', on_delete=models.SET_NULL,
                    null=True, blank=True)

    def __str__(self):
        return self.your_name


class EventType(models.Model):
    name = models.CharField(max_length=54, blank=False, null=False)

    def __str__(self):
        return self.name