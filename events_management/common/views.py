from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import generic as views

from events_management.common.forms import LocationCreateForm
from events_management.common.models import Location
from events_management.event.models import Event, EventRegistration


class GroupRequiredMixin:
    groups_required = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=self.groups_required).exists():
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)


class LocationListView(views.ListView):
    model = Location
    template_name = 'common/index.html'
    context_object_name = 'locations'


class LocationCreateView(GroupRequiredMixin, views.CreateView):
    model = Location
    form_class = LocationCreateForm
    template_name = 'common/location_add.html'

    success_url = reverse_lazy('locations')

    groups_required = ['Staff_EMS', 'Superusers_EMS']


class LocationDeleteView(GroupRequiredMixin, views.DeleteView):
    model = Location
    success_url = reverse_lazy('locations')

    groups_required = ['Superusers_EMS']


class Dashboard(LoginRequiredMixin, views.ListView):
    model = Event
    template_name = 'common/dashboard.html'

    def get_queryset(self):
        profile = self.request.user.pk

        events_created = Event.objects.filter(organizer=profile)

        registered_events_ids = EventRegistration.objects.filter(user=profile).values_list('event_id', flat=True)
        events_registered = Event.objects.filter(id__in=registered_events_ids)

        queryset = list(events_created) + list(events_registered)

        return queryset
