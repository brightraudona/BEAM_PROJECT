from django.shortcuts import render
from django.contrib.auth import logout
from folium import folium
import requests

# Create your views here.
def home(request):
    # Make your map object
    main_map = folium.Map(location=[54.6872, 25.2797], zoom_start = 12) # Create base map
    main_map_html = main_map._repr_html_() # Get HTML for website

    if request.user.is_anonymous:
        return render(request, 'index.html')
    else:
        data = {
            "user":request.user,
            "main_map":main_map_html
        }
        return render(request, 'index.html', data)