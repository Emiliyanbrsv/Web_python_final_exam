from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views

from events_management.event.forms import EventCreateForm, EventRegistrationForm
from events_management.event.models import Location, Event, EventViews, EventRegistration


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()

        context['is_organizer'] = event.organizer.pk == self.request.user.pk
        return context


class EventDeleteView(views.DeleteView):
    model = Event
    success_url = reverse_lazy('locations')
    template_name = 'event/event_delete.html'

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()

        if request.user.pk != event.organizer.pk:
            raise Http404("You are not allowed to delete this event.")

        return super().dispatch(request, *args, **kwargs)


class EventEditView(views.UpdateView):
    model = Event


class RegisterEventView(LoginRequiredMixin, views.CreateView):
    template_name = 'event/event_register.html'
    form_class = EventRegistrationForm
    model = EventRegistration
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        initial = super().get_initial()
        profile = self.request.user.profile
        initial['first_name'] = profile.first_name
        initial['last_name'] = profile.last_name
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        event = get_object_or_404(Event, slug=slug)
        context['event'] = event
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event = self.get_context_data()['event']

        return super().form_valid(form)


class Dashboard(LoginRequiredMixin, views.ListView):
    model = Event
    template_name = 'common/dashboard.html'

    def get_queryset(self):
        profile = self.request.user.pk
        print(profile)

        events_created = Event.objects.filter(organizer=profile)

        # Filter events that the user is registered to via EventRegistration
        registered_events_ids = EventRegistration.objects.filter(user=profile).values_list('event_id', flat=True)
        events_registered = Event.objects.filter(id__in=registered_events_ids)

        # Merge the two querysets to get a single list of events
        queryset = list(events_created) + list(events_registered)

        return queryset
