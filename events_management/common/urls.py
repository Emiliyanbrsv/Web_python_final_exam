from django.urls import path

from events_management.common.views import LocationListView, Dashboard, LocationCreateView, LocationDeleteView

urlpatterns = (
    path('', LocationListView.as_view(), name='locations'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('create-location/', LocationCreateView.as_view(), name='location create'),
    path('delete-location/<int:pk>/', LocationDeleteView.as_view(), name='location delete')
)
