from django.urls import path, include

from events_management.event.views import EventCreateView, EventListView, EventDetailsView, \
    EventDeleteView, RegisterEventView, EventEditView, UnregisterEventView

urlpatterns = (
    path('create/', EventCreateView.as_view(), name='create event'),
    path('<str:city_name>/', EventListView.as_view(), name='location event'),

    path('<slug:slug>/', include([
        path('register/', RegisterEventView.as_view(), name='register event'),
        path('unregister/', UnregisterEventView.as_view(), name='unregister event'),

        path('details/', EventDetailsView.as_view(), name='details event'),
        path('edit/', EventEditView.as_view(), name='edit event'),
        path('delete/', EventDeleteView.as_view(), name='delete event'),
    ])),
)
