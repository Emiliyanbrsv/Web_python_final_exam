from django.contrib.auth import login, get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views import generic as views

from events_management.app_auth.forms import RegisterUserForm

# app_auth models
UserModel = get_user_model()


class AnonymousUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_anonymous


class RegisterUserView(AnonymousUserMixin, views.View):
    form_class = RegisterUserForm
    template_name = 'app_auth/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            login(request, user)

            return redirect('profile_edit', pk=user.pk)

        return render(request, self.template_name, {'form': form})


class LoginUserView(AnonymousUserMixin, auth_views.LoginView):
    template_name = 'app_auth/login.html'


class LogoutUserView(LoginRequiredMixin, auth_views.LogoutView):
    pass


class ChangePasswordView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'app_auth/change_password.html'

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse('profile_details', kwargs={'pk': pk})
