from django.urls import path

from events_management.event.views import LocationListView, EventCreateView, EventListView, EventDetailsView, \
    EventDeleteView, Dashboard, RegisterEventView, EventEditView, UnregisterEventView

urlpatterns = (
    path('', LocationListView.as_view(), name='locations'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('event/create/', EventCreateView.as_view(), name='create event'),

    path('event/<slug:slug>/register/', RegisterEventView.as_view(), name='register event'),
    path('event/<slug:slug>/unregister/', UnregisterEventView.as_view(), name='unregister_event'),

    path('event/<slug:slug>/details', EventDetailsView.as_view(), name='details event'),
    path('event/<slug:slug>/edit', EventEditView.as_view(), name='edit event'),
    path('event/<slug:slug>/delete', EventDeleteView.as_view(), name='delete event'),
    path('events/<str:city_name>/', EventListView.as_view(), name='location event'),
)
