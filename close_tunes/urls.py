from django.contrib import admin
from django.urls import path, include
from . import settings
from player_app import views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('player_app.urls')),
]
