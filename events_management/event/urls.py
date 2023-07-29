from django.urls import path

from events_management.event.views import LocationListView, EventCreateView, EventListView

urlpatterns = (
    path('', LocationListView.as_view(), name='locations'),
    path('event/create/', EventCreateView.as_view(), name='create event'),
    path('events/<str:city_name>/', EventListView.as_view(), name='location event')
    # path('event/<slug:event_slug>/', EventListView.as_view(), name='location event'),
)
