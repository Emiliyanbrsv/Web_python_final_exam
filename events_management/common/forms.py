from django import forms

from events_management.common.models import Location


class LocationCreateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

        widgets = {
            'city_name': forms.TextInput(
                attrs={
                    'placeholder': 'City Name'
                },
            ),
            'country': forms.TextInput(
                attrs={
                    'placeholder': 'Country'
                },
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Description'
                }
            )
        }
