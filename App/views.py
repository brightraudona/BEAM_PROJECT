from django.shortcuts import render
from django.contrib.auth import logout
import requests

# Create your views here.
def home(request):
    # Make your map object
    # main_map = folium.Map(location=[43.45, -80.476], zoom_start = 12) # Create base map
    # main_map_html = main_map._repr_html_() # Get HTML for website

    if request.user.is_anonymous:
        return render(request, 'index.html')

    user = request.user # Pulls in the Strava User data
    strava_login = user.social_auth.get(provider='strava') # Strava login
    #email = strava_login.extra_data['email']
    data = {
        "user":request.user
    }
    return render(request, 'index.html', data)