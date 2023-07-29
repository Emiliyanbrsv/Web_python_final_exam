from django import forms

from events_management.event.models import Event


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        # fields = '__all__'
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
