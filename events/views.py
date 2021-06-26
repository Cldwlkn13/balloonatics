from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .models import Event, EventType
from .forms import EventForm


def events(request):

    if request.method == 'POST':
        
        event_form = EventForm(request.POST)

        form_data = {
            'your_name': request.POST['your_name'],
            'your_email': request.POST['your_email'],
            'your_number': request.POST['your_number'],
            'your_message': request.POST['your_message'],
            'event_type': request.POST['event_type']
        }

        event_type = EventType.objects.get(
            pk=int(form_data['event_type']))

        event_form = EventForm(form_data)

        if not event_form.is_valid():  
            messages.error(request, 
                f'''Your enquiry could not be processed. 
                Please check your information 
                and try again''', 
                extra_tags='render_toast') 
            context = {
                'event_form': event_form,
            }
            return render(request, 'events/events.html', context)   

        event = Event(
            your_name=form_data['your_name'],
            your_email=form_data['your_email'],
            your_number=form_data['your_number'],
            your_message=form_data['your_message'],
            event_type=event_type
        )
        event.save()

        messages.success(request, 
            f'''Thank your for your enquiry! 
            A member of our team will be in 
            touch shortly to discuss.''', 
            extra_tags='render_toast')

        event_form = EventForm()

        context = {
            'event_form': event_form,
            'thank_you': True
        }

        return render(request, 'events/events.html', context)    
 
    event_form = EventForm()
    
    context = {
        'event_form': event_form
    }

    return render(request, 'events/events.html', context)