from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic as views

from events_management.user_profile.forms import NormalProfileEditForm, OrganizerProfileEditForm

# user_profile
UserModel = get_user_model()


class ProfileDetailsView(LoginRequiredMixin, views.DetailView):
    template_name = 'profile/profile_details.html'

    def get_object(self, *args, **kwargs):
        user = self.request.user
        profile_type = user.profile_type

        if profile_type == 'normal':
            return user.profile
        elif profile_type == 'organizer':
            return user.organizer
        else:
            raise Http404("Profile not found.")


class ProfileEditView(LoginRequiredMixin, views.UpdateView):
    template_name = 'profile/profile_edit.html'
    success_url = reverse_lazy('locations')

    def get_object(self, *args, **kwargs):
        user = self.request.user
        profile_type = user.profile_type

        if profile_type == 'normal':
            return user.profile
        elif profile_type == 'organizer':
            return user.organizer
        else:
            raise Http404("Profile not found.")

    def get_form_class(self):
        profile_type = self.request.user.profile_type

        if profile_type == 'normal':
            return NormalProfileEditForm
        elif profile_type == 'organizer':
            return OrganizerProfileEditForm
        else:
            raise Http404("Profile not found.")


class ProfileDeleteView(LoginRequiredMixin, views.DeleteView):
    model = UserModel
    template_name = 'profile/profile_delete.html'

    success_url = reverse_lazy('register_user')
