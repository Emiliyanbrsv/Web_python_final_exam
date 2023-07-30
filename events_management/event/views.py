from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views import generic as views

from events_management.event.forms import EventCreateForm
from events_management.event.models import Location, Event, EventViews


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


def get_total_views(event):
    total_views = EventViews.objects.filter(event=event).aggregate(Sum('views_count'))['views_count__sum']
    return total_views or 0


class EventListView(views.ListView):
    model = Event
    template_name = 'event/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        city_name = self.kwargs.get('city_name')
        return Event.objects.filter(location__city_name=city_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = context['events']
        for event in events:
            event.total_views = get_total_views(event)

        return context


class EventDetailsView(views.DetailView):
    model = Event
    template_name = 'event/event_detail.html'
    context_object_name = 'event'

    def get_object(self, queryset=None):
        event = super().get_object(queryset=queryset)

        if not isinstance(self.request.user, AnonymousUser):
            event_view, created = EventViews.objects.get_or_create(event=event, user=self.request.user)
            if not created:
                event_view.views_count += 1
                event_view.save()

        return event


class EventDeleteView(views.DeleteView):
    model = Event
    success_url = reverse_lazy('locations')
    template_name = 'event/event_delete.html'

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer


class EventEditView(views.UpdateView):
    model = Event


class RegisterEventView(LoginRequiredMixin, views.CreateView):
    pass
