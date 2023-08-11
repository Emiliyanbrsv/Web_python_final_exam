from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from events_management.event.forms import EventCreateForm, EventRegistrationForm, EventEditForm
from events_management.event.models import Event, EventViews, EventRegistration
from events_management.utils.utils import send_sms


# event_views
class NormalUserMixin(UserPassesTestMixin):
    login_url = reverse_lazy('login_user')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile_type == 'normal'


class OrganizerRequiredMixin(UserPassesTestMixin):
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile_type == 'organizer'


class EventCreateView(LoginRequiredMixin, OrganizerRequiredMixin, views.CreateView):
    form_class = EventCreateForm
    template_name = 'event/event_create.html'

    success_url = reverse_lazy('locations')

    def form_valid(self, form):
        form.instance.organizer = self.request.user.organizer
        return super().form_valid(form)


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


def get_total_views(event):
    total_views = EventViews.objects.filter(event=event).aggregate(Sum('views_count'))['views_count__sum']
    return total_views or 0


class EventDetailsView(views.DetailView):
    model = Event
    template_name = 'event/event_detail.html'
    context_object_name = 'event'

    def get_object(self, queryset=None):
        if not hasattr(self, '_event'):
            event = super().get_object(queryset=queryset)

            if not isinstance(self.request.user, AnonymousUser):
                event_view, created = EventViews.objects.get_or_create(event=event, user=self.request.user)
                if created:
                    event_view.views_count = 1
                else:
                    event_view.views_count += 1
                event_view.save()

            self._event = event
        return self._event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()

        if self.request.user.is_authenticated:
            context['is_organizer'] = event.organizer.pk == self.request.user.pk
            context['user_registered'] = event.is_registered(self.request.user)
        return context


class EventDeleteView(LoginRequiredMixin, OrganizerRequiredMixin, views.DeleteView):
    model = Event
    success_url = reverse_lazy('locations')
    template_name = 'event/event_delete.html'

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()

        if request.user.pk != event.organizer.pk:
            raise Http404("You are not allowed to delete this event.")

        return super().dispatch(request, *args, **kwargs)


class EventEditView(LoginRequiredMixin, OrganizerRequiredMixin, views.UpdateView):
    model = Event
    form_class = EventEditForm
    template_name = 'event/event_edit.html'

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()

        if request.user.pk != event.organizer.pk:
            raise Http404("You are not allowed to edit this event.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        slug = self.object.slug
        return reverse('details event', kwargs={'slug': slug})


class RegisterEventView(LoginRequiredMixin, NormalUserMixin, views.CreateView):
    template_name = 'event/event_register.html'
    form_class = EventRegistrationForm
    model = EventRegistration
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        initial = super().get_initial()
        profile = self.request.user.profile
        initial['first_name'] = profile.first_name
        initial['last_name'] = profile.last_name
        initial['phone_number'] = profile.phone_number
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

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     event = self.get_context_data()['event']
    #     form.instance.event = event

    #     response = super().form_valid(form)

    #     phone_number = f'+{self.request.user.profile.phone_number}'
    #     message = f"Thank you for attending {event.name}. Have a nice day {self.request.user.profile.first_name}!"

    #     send_sms(phone_number, message)

    #     return response


class UnregisterEventView(LoginRequiredMixin, NormalUserMixin, views.View):
    def get(self, request, *args, **kwargs):
        return redirect('details event', slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        event = get_object_or_404(Event, slug=slug)

        try:
            registration = EventRegistration.objects.get(user=request.user, event=event)
            registration.delete()
        except EventRegistration.DoesNotExist:
            pass

        return redirect('details event', slug=slug)
