# user_profile
from django.urls import path

from events_management.user_profile.views import ProfileDetailsView, ProfileEditView, ProfileDeleteView

urlpatterns = (
    path('details/<int:pk>/', ProfileDetailsView.as_view(), name='profile_details'),
    path('edit/<int:pk>/', ProfileEditView.as_view(), name='profile_edit'),
    path('delete/<int:pk>', ProfileDeleteView.as_view(), name='profile_delete'),
)
