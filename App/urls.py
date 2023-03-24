from django.contrib.auth.views import LogoutView
from django.urls import path, include

from StravaWebsite import settings
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('challenge/<challengeId>', challenge, name='challenge' ),
    path('join_challenge/', join_challenge, name='join_challenge'),
]