from django import forms

from events_management.user_profile.models import Profile, Organizer


class NormalProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name'
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Last Name'
                },
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'placeholder': 'Phone Number'
                },
            ),
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

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Name'
                },
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Description'
                },
            ),
            'website': forms.URLInput(
                attrs={
                    'placeholder': 'Website'
                },
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'placeholder': 'Phone number'
                },
            ),
        }
