from django.contrib.auth import login, get_user_model
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect

from django.views import generic as views

from events_management.app_auth.forms import RegisterUserForm

# app_auth models
UserModel = get_user_model()


class RegisterUserView(views.View):
    form_class = RegisterUserForm
    template_name = 'app_auth/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set any additional fields as needed
            user.save()

            # Log in the user
            login(request, user)

            # Redirect to the profile details page with the user's pk
            return redirect('profile_edit', pk=user.pk)

        return render(request, self.template_name, {'form': form})

    # success_url = reverse_lazy('locations')

    # def form_valid(self, form):
    #     result = super().form_valid(form)
    #
    #     login(self.request, self.object)
    #
    #     return result
    #
    # def get_success_url(self):
    #     pk = self.request.user.pk
    #     return reverse('profile_details', kwargs={'pk': pk})


class LoginUserView(auth_views.LoginView):
    template_name = 'app_auth/login.html'


class LogoutUserView(auth_views.LogoutView):
    pass
