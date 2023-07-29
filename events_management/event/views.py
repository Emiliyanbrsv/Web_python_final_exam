from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic as views

from events_management.event.forms import EventCreateForm
from events_management.event.models import Location, Event


# event_views
#
class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile_type == 'organizer'


class LocationListView(views.ListView):
    model = Location
    template_name = 'event/locations.html'


class LocationCreateView(views.CreateView):
    pass


class EventCreateView(OrganizerRequiredMixin, views.CreateView):
    form_class = EventCreateForm
    template_name = 'event/event_create.html'

    success_url = reverse_lazy('locations')

    def form_valid(self, form):
        form.instance.organizer = self.request.user.organizer
        return super().form_valid(form)


class EventListView(views.ListView):
    model = Event
    template_name = 'event/event_list.html'

    def get_queryset(self):
        city_name = self.kwargs.get('city_name')
        return Event.objects.filter(location__city_name=city_name)


class EventDetailsView(views.DetailView):
    pass


class EventDeleteView(views.DeleteView):
    model = Event


class RegisterEventView(LoginRequiredMixin, views.CreateView):
    pass
