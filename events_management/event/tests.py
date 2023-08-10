from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from events_management.app_auth.models import AppUser
from events_management.common.models import Location
from events_management.event.forms import EventCreateForm
from events_management.event.models import Event
from events_management.event.views import EventCreateView
from events_management.user_profile.models import Organizer


class EventCreateViewTests(TestCase):
    def setUp(self):
        # Create a test user and organizer
        self.user = AppUser.objects.create_user(email='testuser', password='testpassword')
        self.organizer = Organizer.objects.create(user=self.user, name='Test Organizer')

        # Create a test location for the event
        self.location = Location.objects.create(city_name='Test City', country='Test Country')

    def test_event_create_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/event_create.html')
        self.assertIsInstance(response.context['view'], EventCreateView)
        self.assertIsInstance(response.context['form'], EventCreateForm)

    def test_event_create_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'name': 'Test Event',
            'start_date_time': '2023-06-30 10:00:00',
            'end_date_time': '2023-06-30 12:00:00',
            'description': 'Test description',
            'location': self.location.pk,
        }
        response = self.client.post(reverse('create event'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertRedirects(response, reverse('locations'))

        # Check if the event is created with the correct organizer
        created_event = Event.objects.get(name='Test Event')
        self.assertEqual(created_event.organizer, self.organizer)

    def test_event_create_view_permission(self):
        # Test that an unauthorized user cannot access the view
        response = self.client.get(reverse('create event'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    # Add more test methods as needed

# More test classes for other views
