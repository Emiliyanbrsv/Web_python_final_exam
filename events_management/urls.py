from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events_management.app_auth.urls')),
    path('', include('events_management.event.urls')),
    path('profile/', include('events_management.user_profile.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
