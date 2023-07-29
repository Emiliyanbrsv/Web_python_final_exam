from django.contrib.auth import login, get_user_model
from django.contrib.auth import views as auth_views

from django.urls import reverse_lazy, reverse
from django.views import generic as views

from events_management.app_auth.forms import RegisterUserForm

# app_auth models
UserModel = get_user_model()


class RegisterUserView(views.CreateView):
    form_class = RegisterUserForm
    template_name = 'app_auth/register.html'

    success_url = reverse_lazy('locations')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result

    # def get_success_url(self):
    #     return reverse('profile_details', kwargs={'pk': self.request.user.pk})


class LoginUserView(auth_views.LoginView):
    template_name = 'app_auth/login.html'


class LogoutUserView(auth_views.LogoutView):
    pass
