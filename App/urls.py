from django.urls import path, include

from StravaWebsite import settings
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('logout/', logout, name='logout'),
]