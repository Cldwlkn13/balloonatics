from events.models import Event
from django import forms

from .models import Event, EventType

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        event_types = list(EventType.objects.all())
        choices = [(et.id, et.name) for et in event_types]
        self.fields['event_type'].choices = choices