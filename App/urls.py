from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('connected/', connected_strava, name='Connect to stravia'),
    path('oauth/', include('social_django.urls', namespace='social')),
]