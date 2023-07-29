from django.urls import path

from events_management.app_auth.views import RegisterUserView, LoginUserView, LogoutUserView

# app_auth urls
urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user')
)
