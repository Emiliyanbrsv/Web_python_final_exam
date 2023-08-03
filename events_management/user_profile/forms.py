from django import forms

from events_management.user_profile.models import Profile, Organizer


class NormalProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={
                    'placeholder': 'mm/dd/yyyy',
                    'type': 'date',
                }
            ),
        }


class OrganizerProfileEditForm(forms.ModelForm):
    class Meta:
        model = Organizer
        exclude = ['user']
