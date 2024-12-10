from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home', views.home_view, name='home'),
    path('play/<path:query>/', views.play_song, name='play_song'),  
]

