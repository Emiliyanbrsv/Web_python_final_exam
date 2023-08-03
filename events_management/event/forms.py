from django import forms

from events_management.event.models import Event, EventRegistration


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer']

        widgets = {
            'start_date_time': forms.DateTimeInput(
                attrs={
                    'placeholder': 'dd/mm/yyyy hh:mm',
                    'type': 'datetime-local',
                },
            ),
            'end_date_time': forms.DateTimeInput(
                attrs={
                    'placeholder': 'dd/mm/yyyy hh:mm',
                    'type': 'datetime-local',
                },
            ),
        }


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['first_name', 'last_name', 'attendees', 'phone_number']
